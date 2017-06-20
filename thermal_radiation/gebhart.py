from itertools import product
from math import isclose
from warnings import warn
import numpy as np

class Surface:
    def __init__(self, name, area, eps):
        self.name = name
        self.area = area
        self.eps = eps       # emissivity
        self.rho = 1.0 - eps # reflectivity

    def __str__(self):
        return f"Surface({self.name})"

    def __repr__(self):
        rtrn_str  = str(self) + ":\n"
        rtrn_str += f"\tarea: {self.area}\n"
        rtrn_str += f"\teps : {self.eps}"
        return rtrn_str


def calc_other_ff(area1, area2, ff12):
    return (area1 * ff12) / area2


class RadiationConnection:
    def __init__(self, surf1, surf2, ff12=None, ff21=None):
        self.surf1 = surf1
        self.surf2 = surf2

        if ff12 is not None:
            self.ff12 = ff12
            self.ff21 = calc_other_ff(surf1.area, surf2.area, ff12)
        elif ff21 is not None:
            self.ff21 = ff21
            self.ff12 = calc_other_ff(surf2.area, surf1.area, ff21)
        else:
            raise Exception("A form factor was not provided.")

    def _same(self, other):
        return (self.surf1 is other.surf1) and (self.surf2 is other.surf2)

    def _inv_same(self, other):
        return (self.surf1 is other.surf2) and (self.surf2 is other.surf1)

    def __eq__(self, other):
        return self._same(other) or self._inv_same(other)

    def __str__(self):
        things = [self.surf1, self.surf2]
        things.sort(key=lambda surf: surf.name)
        first, second = things
        rtrn_str  = f"RadiationConnection({first}, {second})"
        return rtrn_str

    def __repr__(self):
        rtrn_str  = str(self) + ":\n"
        rtrn_str += "\t" + str(self.surf1) + "->" + str(self.surf2) + ": " + str(self.ff12) + "\n"
        rtrn_str += "\t" + str(self.surf2) + "->" + str(self.surf1) + ": " + str(self.ff21)
        return rtrn_str

    def get_view_factor(self, from_surf, to_surf):
        surf1_name = self.surf1.name
        surf2_name = self.surf2.name
        if from_surf == surf1_name and to_surf == surf2_name:
            return self.ff12
        else:
            return self.ff21

    def __add__(self, other):
        if self == other:
            if self._same(other):
                self.ff12 += other.ff12
                self.ff21 += other.ff21
                return self
            else:
                self.ff12 += other.ff21
                self.ff21 += other.ff12
                return self


class NoConnectionException(Exception):
    def __init__(self, from_surf, to_surf):
        Exception.__init__(self, f"No connection from {from_surf} to {to_surf}")


class NoSurfaceException(Exception):
    def __init__(self, surf_name):
        Exception.__init__(self, f"No surface named \"{surf_name}\" in the thermal network.")


class ThermalNetwork:
    def __init__(self, name=None):
        self.name = name
        self.surfaces = {} # surface name -> surface properties
        self.rad_connections = {} # surface name -> surface name -> RadiationConnection

    def add_surface(self, name, area, eps):
        self.surfaces[name] = Surface(name, area, eps)

    def _add_rad_connection_group(self, surf1_name, surf2_name, connection):
        if surf1_name not in self.rad_connections:
            self.rad_connections[surf1_name] = {surf2_name : connection}
        else:
            if surf2_name in self.rad_connections[surf1_name]:
                self.rad_connections[surf1_name][surf2_name] += connection
            else:
                self.rad_connections[surf1_name][surf2_name] = connection

    def add_rad_connections(self, surf1_name, surf2_name, ff12=None, ff21=None):
        surf1 = self.surfaces[surf1_name]
        surf2 = self.surfaces[surf2_name]
        connection =  RadiationConnection(surf1, surf2, ff12=ff12, ff21=ff21)
        self._add_rad_connection_group(surf1_name, surf2_name, connection)
        self._add_rad_connection_group(surf2_name, surf1_name, connection)

    def _get_rad_connection(self, surf1_name, surf2_name):
        if surf1_name not in self.surfaces:
            raise NoSurfaceException(surf1_name)

        if surf2_name not in self.surfaces:
            raise NoSurfaceException(surf2_name)

        try:
            return self.rad_connections[surf1_name][surf2_name]
        except:
            raise NoConnectionException(surf1_name, surf2_name)

    def get_view_factor(self, surf1_name, surf2_name):
        try:
            rad_connection = self._get_rad_connection(surf1_name, surf2_name)
            return rad_connection.get_view_factor(surf1_name, surf2_name)
        except NoConnectionException:
            return 0.0
        except NoSurfaceException as exp:
            raise exp

    def surface_combinations(self):
        return product(self.surfaces, self.surfaces)

    def get_view_factors_sums(self):
        view_factor_sums = {surface : 0.0  for surface in self.surfaces}
        for from_surf, to_surf in self.surface_combinations():
            view_factor_sums[from_surf] += self.get_view_factor(from_surf, to_surf)
        return view_factor_sums # from surface -> total view factor accounted for

    def verify_view_factors(self, view_factor_sums=None):
        view_factor_sums = self.get_view_factors_sums() if view_factor_sums is None else view_factor_sums
        for from_surf, sum_ in view_factor_sums.items():
            if not isclose(sum_, 1.0):
                warn(f"View factors from {from_surf} is not close to 1.0. It is {sum_}.")

    def matrix_build_indexer(self):
        n = len(self.surfaces)
        for number, (from_surf, to_surf) in enumerate(self.surface_combinations()):
            i, j = divmod(number, n)
            yield (i, from_surf), (j, to_surf)

    def reflected_term(self, from_surf, to_surf): # reflected from {from_surf} to {to_surf}
        reflectivity = self.surfaces[from_surf].rho
        view_factor  = self.get_view_factor(from_surf, to_surf)
        return -1.0 * reflectivity * view_factor

    def build_gebhart_slae(self, to_surf):
        n = len(self.surfaces)
        A = np.empty((n, n))
        b = np.empty(n)
        for (i, loc_from_surf), (j, loc_to_surf) in self.matrix_build_indexer():
            A[i, j] = self.reflected_term(loc_from_surf, loc_to_surf)
            if i == j:
                A[i, j] += 1.0

        eps_to = self.surfaces[to_surf].eps
        for i, from_surf in enumerate(self.surfaces):
            b[i] = eps_to * self.get_view_factor(from_surf, to_surf)

        return A, b

    def get_grey_body_factors(self):
        n = len(self.surfaces)
        gbf_map = {} # name (from) -> name (to) -> factor

        for to_indx, to_surf in enumerate(self.surfaces):
            A, b = self.build_gebhart_slae(to_surf)
            x = np.linalg.solve(A, b)

            for from_indx, from_surf in enumerate(self.surfaces):
                if to_indx == 0:
                    gbf_map[from_surf] = {}
                gbf_map[from_surf][to_surf] = x[from_indx]

        return gbf_map

    def get_radks(self, gbf_map):
        radks_map = {}
        for from_surf, to_surf_factors in gbf_map.items():
            from_surf_val = self.surfaces[from_surf]
            from_area = from_surf_val.area
            from_eps = from_surf_val.eps

            to_map = {}
            for to_surf, grey_body_factor in to_surf_factors.items():
                to_map[to_surf] = from_eps * from_area * grey_body_factor

            radks_map[from_surf] = to_map

        return radks_map


if __name__ == '__main__':


    print("tri-parallel plates")

    eps = 0.05

    tn = ThermalNetwork()
    tn.add_surface("surf1", 1.0, eps)
    tn.add_surface("surf2", 1.0, eps)
    tn.add_surface("surf3", 1.0, eps)

    tn.add_rad_connections("surf1", "surf2", ff12=0.5)
    tn.add_rad_connections("surf1", "surf3", ff12=0.5)
    tn.add_rad_connections("surf2", "surf3", ff12=0.5)

    tn.verify_view_factors()

    gbf_map  = tn.get_grey_body_factors()
    radk_map = tn.get_radks(gbf_map)

    def print_factors(from_surf, to_surf):
        print(f"from {from_surf} to {to_surf} :", gbf_map[from_surf][to_surf])

    for from_surf, to_surf in tn.surface_combinations():
        print_factors(from_surf, to_surf)
