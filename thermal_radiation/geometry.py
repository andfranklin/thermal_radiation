import numpy as np
from scipy.integrate import nquad
from math import isclose

def about_zero(num):
    return isclose(0.0, num, abs_tol=1.0E-14)

def magnitude(vec):
    return np.sqrt(vec @ vec)


def normalize(vec):
    return vec / magnitude(vec)


def get_displacement_vector(from_vec, to_vec):
    return to_vec - from_vec


def get_direction(from_vec, to_vec):
    return normalize(get_displacement_vector(from_vec, to_vec))


def classify_cross_product(from_vertex, to_vertex, point):
    from_to_point = point - from_vertex
    from_to_to = to_vertex - from_vertex
    cross = np.cross(from_to_point, from_to_to)
    mag = cross @ cross
    up = mag > 0.0
    down = mag < 0.0
    zero = mag == 0.0
    return up, down, zero


class Triangle:
    def __init__(self, a, b, c):
        """
        Args:
            a, b, c (vectors): The position vectors representing the vertices
                oriented in the counter clockwise orientation w.r.t. the surface
                normal.

        e.g. if the normal is coming out of the computer screen

            eta
            c
            | \
            |  \
            |   \
            a____b Xi
        """
        self.a = np.array(a)
        self.b = np.array(b)
        self.c = np.array(c)

        disp_a_to_b = get_displacement_vector(self.a, self.b)
        disp_a_to_c = get_displacement_vector(self.a, self.c)
        cross = np.cross(disp_a_to_b, disp_a_to_c)
        cross_mag = magnitude(cross)
        assert not about_zero(cross_mag) # 0.0 iff all points are in a line -- the points don't specify a triangle

        self.area = 0.5 * cross_mag
        self.normal = cross
        self.normalized_normal = cross / cross_mag
        self.magnitude = cross_mag
        self.centroid = (self.a + self.b + self.c) / 3.0

    def project_onto(self, point):
        """
        Project point onto the place of the triangle using least squares
        """
        aT = np.array([self.a, self.b])
        a = aT.T
        A = aT @ a
        b = aT @ point
        point_in_plane = np.linalg.solve(A, b)
        return a @ point_in_plane

    def point_on(self, point, project_first=False):
        point = self.project_onto(point) if project_first else point

        a_up, a_down, a_zero = classify_cross_product(self.a, self.b, point)
        b_up, b_down, b_zero = classify_cross_product(self.b, self.c, point)
        c_up, c_down, c_zero = classify_cross_product(self.c, self.a, point)

        on_edge = a_zero or b_zero or c_zero
        on_vertex = on_edge and ((a_zero and b_zero) or (a_zero and c_zero) or (b_zero and c_zero))

        all_up = a_up and b_up and c_up
        all_down = a_down and b_down and c_down
        inside = all_up or all_down

        return on_edge or on_vertex or inside

    def surface_location(self, xi, eta):
        assert xi <= 1.0 and xi >= 0.0
        assert eta <= 1.0 and eta >= 0.0
        assert xi + eta <= 1.0
        r  = (1.0 - xi - eta) * self.a
        r += xi * self.b
        r += eta * self.c
        return r

    def split(self):
        """
        Split using a as the splitting node
        """
        dir_a_to_b = get_direction(self.a, self.b)
        dir_a_to_c = get_direction(self.a, self.c)
        dir_a_to_steiner = 0.5 * (dir_a_to_b + dir_a_to_c)
        line_a_to_steiner = Line(self.a, dir_a_to_steiner)

        line_c_to_b = Line(self.c, get_direction(self.c, self.b))


class DegenerateIntersection(Exception):
    """
    Should be thrown in the scenario when the intersection of two generalized
    hyperplanes is trying to be found but a degenerate case has occured. The
    possible degenerate cases:
        1) The hyperplanes are overlayed (e.g. two planes that are infact the same).
        2) The hyperplanes are parallel and never intersect.
    """
    def __init__(self):
        Except.__init__(self, "Degenerate intersection occured")


class Line:
    def __init__(self, point, direction):
        self.point = np.array(point)
        self.direction = np.array(direction)

    def get_point(self, t):
        return self.point + (self.direction * t)

    def get_distance_to_plane(self, plane):
        numer = plane.normalized_normal @ (plane.a - self.point)
        denom = plane.normalized_normal @ self.direction
        if about_zero(denom):
            raise DegenerateIntersection()
        return numer / denom

    def get_intersection_info(self, plane):
        """
        Args:
            plane (Triangle): The plane which the line may intersect.

        Returns:
            float: The distance from the line origin to the intersection.
            vector: The position vector of the point in 3D space.

        Raises:
            DegenerateIntersection
        """
        try:
            t = self.get_distance_to_plane(plane)
            return t, self.get_point(t)
        except DegenerateIntersection as di:
            raise di
            return 0.0, self.point


def get_intersection_point(line1, line2):
    plane_normal = np.cross(line1.direction, line2.direction)
    if about_zero(magnitude(plane_normal)):
        raise DegenerateIntersection()

    line2_planer_normal = np.cross(plane_normal, line2.direction)
    denom = line1.direction @ line2_planer_normal
    if about_zero(denom):
        raise DegenerateIntersection()

    line2_to_line1 = get_displacement_vector(line2.point, line1.point)
    distance = (-1.0 * (line2_to_line1 @ line2_planer_normal)) / denom
    return line1.get_point(distance)

#
#     # aT = np.array([self.a, self.b])
#     # a = aT.T
#     # A = aT @ a
#     # b = aT @ point
#     # point_in_plane = np.linalg.solve(A, b)
#     # return a @ point_in_plane


def general_diff_view_factor(from_r, from_n, to_r, to_n):
    """ The differential view factor between to differential areas
    Args:
        from_r (vector): The position vector of the differential surface which the radiation is emitted.
        from_n (unit vector): The surface normal correspoinding to from_r.
        to_r (vector): The position vector of the differential surface which the radiation is intercepted.
        to_n (unit vector): The surface normal correspoinding to to_r.

    Returns:
        float: The differential view factor between the differential areas.
    """
    s = to_r - from_r
    s_squared = s @ s
    numerator = -1.0 * (from_n @ s) * (to_n @ s)
    denom = np.pi * s_squared * s_squared
    return numerator / denom


def generate_triangles_diff_view_factor(from_triangle, to_triangle):
    from_n = from_triangle.normalized_normal
    to_n = to_triangle.normalized_normal

    def triangle_diff_view_factor(from_xi, from_eta, to_xi, to_eta):
        from_r = from_triangle.surface_location(from_xi, from_eta)
        to_r = to_triangle.surface_location(to_xi, to_eta)
        return general_diff_view_factor(from_r, from_n, to_r, to_n)

    return triangle_diff_view_factor


def xi_constraint(eta):
    return 1.0 - eta

def from_xi_constraint(from_eta, to_xi, to_eta):
    return (0.0, xi_constraint(from_eta))

def to_xi_constraint(to_eta):
    return (0.0, xi_constraint(to_eta))

quad_bounds = [from_xi_constraint, (0, 1), to_xi_constraint, (0, 1)]

def get_triangle_view_factor(from_triangle, to_triangle, epsabs=1.0e-08, epsrel=1.0e-08, limit=50):
    """
    epsabs : float or int, optional
        Absolute error tolerance.
    epsrel : float or int, optional
        Relative error tolerance.
    limit  : float or int, optional
        An upper bound on the number of subintervals used in the adaptive algorithm.
    """

    quad_scale = 4.0 * from_triangle.area * to_triangle.area

    opts = {
        "epsabs" : epsabs / quad_scale,
        "epsrel" : epsrel,
        "limit" : limit,
    }

    triangle_diff_view_factor = generate_triangles_diff_view_factor(from_triangle, to_triangle)
    ref_quad, error = nquad(triangle_diff_view_factor, quad_bounds, opts=opts)
    return (quad_scale * ref_quad) / from_triangle.area


if __name__ == '__main__':
    from math import tan, radians
    import matplotlib.pyplot as plt
    from time import time
    import pickle

    def print_triangle(name, triangle):
        print(f"Triangle {name}")
        print(f"  area    : {triangle.area}")
        print(f"  centroid: {triangle.centroid}")
        print(f"  normal  : {triangle.normalized_normal}")

    # a = Triangle([0, 0, 0], [1, 0, 0], [0, 1, 0])
    # b = Triangle([0, 0, 1], [0, 1, 1], [1, 0, 1])
    #
    # print_triangle("A", a); print()
    # print_triangle("B", b); print()
    # print(get_triangle_view_factor(a, b))

    def apprx_parallel_directly_opposed_triangles(normalized_distance, theta):
        base = 1.0
        distance = base * normalized_distance
        height = tan(radians(theta)) * base

        triangle1 = Triangle(
            [0.0,  0.0, 0.0   ], # a
            [0.0,  0.0, height], # b
            [base, 0.0, 0.0   ]  # c
        )

        # print_triangle("triangle1", triangle1); print()

        triangle2 = Triangle(
            [0.0,  distance, 0.0   ], # a
            [base, distance, 0.0   ], # b
            [0.0,  distance, height]  # c
        )

        # print_triangle("triangle2", triangle2); print()

        return get_triangle_view_factor(triangle1, triangle2)

    def pickle_data(file_name, data):
        with open(file_name, mode="wb") as pckl_file:
            pickle.dump(data, pckl_file)

    relative_distaces = np.linspace(0.1, 10.0, 20)
    angle = 75.0
    view_factors = []

    rds = []
    times = []
    angle_view_factors = []
    for relative_distace in relative_distaces:
        print(angle, relative_distace, end=" : \n")
        begin = time()
        view_factor = apprx_parallel_directly_opposed_triangles(relative_distace, angle)
        angle_view_factors.append(view_factor)
        end = time()
        total = end - begin
        times.append(total)
        rds.append(relative_distace)
        print(f"\t{view_factor:.10f} {total:.3f}")
    # plt.plot(relative_distaces, angle_view_factors, label=f"${angle:2.0f}^o$")

    angle_posfix = f"{angle:2.0f}.pkl"
    pickle_data("view_factors_" + angle_posfix, angle_view_factors)
    pickle_data("times_" + angle_posfix, times)
    pickle_data("relative_dists_" + angle_posfix, rds)


    # plt.legend()
    # plt.xscale('log')
    # plt.savefig('right_triangles.pdf')
    # plt.show()

    # sol = apprx_parallel_directly_opposed_triangles(1.0, 75.0)
    # print(sol)