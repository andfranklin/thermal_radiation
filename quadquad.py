from time import time
from thermal_radiation.quadrature_2d import TriangleTensorProductGaussLegendre2D, TriangleSymmetricalGauss2D
from thermal_radiation.geometry import Triangle, adaptive_triangle_view_factor, get_fixed_triangle_view_factor
from thermal_radiation.view_factors import two_coaxial_parallel_plates

adaptive_abs_tol     = 1.0e-16
adaptive_rel_tol     = 1.0e-10
adaptive_iter_lim    = 1000
tensor_poduct_order  = 30
symmetric_quad_order = 13 # 13 is the maximum
print_n_digits = 54

# quad 1
triangle1 = Triangle(
        [0.0, 5.0, 0.0], # a
        [2.0, 5.0, 0.0], # b
        [2.0, 7.0, 0.0]  # c
    )

triangle2 = Triangle(
        [0.0, 5.0, 0.0], # a
        [2.0, 7.0, 0.0], # c
        [0.0, 7.0, 0.0]  # d
    )

quad1_area = triangle1.area + triangle2.area

# quad 2
triangle3 = Triangle(
        [0.0, 5.0, 1.0], # a
        [0.0, 7.0, 1.0], # b
        [2.0, 7.0, 1.0]  # c
    )

# quad 2
triangle4 = Triangle(
        [0.0, 5.0, 1.0], # a
        [2.0, 7.0, 1.0], # c
        [2.0, 5.0, 1.0]  # d
    )

quad2_area = triangle3.area + triangle4.area

# ------------------------------------------------------------------------------

configured_adaptive_triangle_view_factor = lambda x, y : adaptive_triangle_view_factor(x, y, epsabs=adaptive_abs_tol, epsrel=adaptive_rel_tol, limit=adaptive_iter_lim)

tensor_quad = TriangleTensorProductGaussLegendre2D(tensor_poduct_order, tensor_poduct_order)
tensor_triangle_view_factor = get_fixed_triangle_view_factor(tensor_quad)

symmetric_quad = TriangleSymmetricalGauss2D(symmetric_quad_order)
symmetric_triangle_view_factor = get_fixed_triangle_view_factor(symmetric_quad)

float_fmt = f".{print_n_digits}f"

print("analytic solution")
analytic_solution = two_coaxial_parallel_plates(2, 2, 1)
print(format(analytic_solution, float_fmt))
print()

def do_view_factor_calc(view_factor_function):
    begin = time()

    tri1tri3 = view_factor_function(triangle1, triangle3)
    tri1tri4 = view_factor_function(triangle1, triangle4)
    tri1quad2 = tri1tri3 + tri1tri4
    quad2tri1 = (tri1quad2 * triangle1.area) / quad2_area

    tri2tri3 = view_factor_function(triangle2, triangle3)
    tri2tri4 = view_factor_function(triangle2, triangle4)
    tri2quad2 = tri1tri3 + tri1tri4
    quad2tri2 = (tri2quad2 * triangle2.area) / quad2_area

    quad2quad1 = quad2tri1 + quad2tri2
    quad1quad2 = (quad2quad1 * quad2_area) / quad1_area

    end = time()
    elapsed_time = end - begin
    print("time :", elapsed_time)
    print("from 1 to 2 :", format(quad1quad2, float_fmt))
    print("abs diff    :", abs(analytic_solution - quad1quad2))

print("adaptive quadrature")
do_view_factor_calc(configured_adaptive_triangle_view_factor)
print()

print("tensor product quadrature")
do_view_factor_calc(tensor_triangle_view_factor)
print()

print("symmetric quadrature")
do_view_factor_calc(symmetric_triangle_view_factor)
