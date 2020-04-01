from .geometry import Triangle

class TriangleElement(Triangle):
    def __init__(self, a, b, c, quadrature):
        Triangle.__init__(self, a, b, c)
        self.quadrature = quadrature
        self.view_factors = {} # element -> view factor to the element
        self.total_view_factor = 0.0

    def add_view_factor(self, element, view_factor):
        self.total_view_factor += view_factor
        self.view_factors[element] = view_factor


class Surface:
    def __init__(self):
        self.elements = []
        self.subsurfaces = []

    def add_element(self, element):
        self.elements.append(element)

    def add_subsurface(self, subsurface):
        self.subsurfaces.append(subsurface)

    def aggregate_elements(self):
        all_elements = self.elements[:]
        for subsurface in self.subsurfaces:
            all_elements += subsurface.aggregate_elements()
        return all_elements


class Problem:
    def __init__(self, surfaces=[]):
        self.surfaces = surfaces

    def add_surface(self, surface):
        self.surfaces.append(surface)

    def aggregate_elements(self):
        elements = []
        for surface in self.surfaces:
            elements += surface.aggregate_elements()
        self.elements = elements

    def calculate_view_factor(self, from_element, to_element):
        return 1.0

    def calculate_view_factors(self):
        for i, from_element in enumerate(self.elements):
            for to_element in self.elements[i+1:]:
                f_from_to = self.calculate_view_factor(from_element, to_element)
                from_element.add_view_factor(to_element, f_from_to)

                f_to_from = (f_from_to * from_element.area) / to_element.area
                to_element.add_view_factor(from_element, f_to_from)


if __name__ == '__main__':
    from .geometry import Triangle

    def print_triangle(triangle):
        print("centroid:", triangle.centroid)
        print("area    :", triangle.area)
        print("normal  :", triangle.normalized_normal)


    s1 = Surface()
    s1.add_element(TriangleElement(
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.0, 1.0, 0.0], None
    ))
    s1.add_element(TriangleElement(
        [1.0, 1.0, 0.0],
        [0.0, 1.0, 0.0],
        [1.0, 0.0, 0.0], None
    ))

    for triangle in s1.elements:
        print_triangle(triangle)
        print()

    s2 = Surface()
    s2.add_element(TriangleElement(
        [0.0, 0.0, 2.0],
        [0.0, 1.0, 2.0],
        [1.0, 0.0, 2.0], None
    ))
    s2.add_element(TriangleElement(
        [1.0, 1.0, 2.0],
        [1.0, 0.0, 2.0],
        [0.0, 1.0, 2.0], None
    ))

    print()
    for triangle in s2.elements:
        print_triangle(triangle)
        print()

    problem = Problem([s1, s2])
