from time import time
from thermal_radiation.quadrature_2d import TriangleTensorProductGaussLegendre2D, TriangleSymmetricalGauss2D
from thermal_radiation.geometry import Triangle, adaptive_triangle_view_factor, get_fixed_triangle_view_factor

adaptive_abs_tol     = 1.0e-16
adaptive_rel_tol     = 1.0e-10
adaptive_iter_lim    = 1000
tensor_poduct_order  = 30
symmetric_quad_order = 13 # 13 is the maximum
print_n_digits = 54

triangle1 = Triangle(
        [0.0, 0.0, 0.0], # a
        [1.0, 0.0, 0.0], # b
        [0.0, 1.0, 0.0]  # c
    )

triangle2 = Triangle(
        [0.0, 0.0, 1.0], # a
        [0.0, 1.0, 1.0], # b
        [1.0, 0.0, 1.0]  # c
    )

# ------------------------------------------------------------------------------

configured_adaptive_triangle_view_factor = lambda x, y : adaptive_triangle_view_factor(x, y, epsabs=adaptive_abs_tol, epsrel=adaptive_rel_tol, limit=adaptive_iter_lim)

tensor_quad = TriangleTensorProductGaussLegendre2D(tensor_poduct_order, tensor_poduct_order)
tensor_triangle_view_factor = get_fixed_triangle_view_factor(tensor_quad)

symmetric_quad = TriangleSymmetricalGauss2D(symmetric_quad_order)
symmetric_triangle_view_factor = get_fixed_triangle_view_factor(symmetric_quad)

float_fmt = f".{print_n_digits}f"

def do_view_factor_calc(view_factor_function):
    begin = time()
    solution12 = view_factor_function(triangle1, triangle2)
    solution21 = view_factor_function(triangle2, triangle1)
    end = time()
    elapsed_time = end - begin
    print("time :", elapsed_time)
    print("from 1 to 2 :", format(solution12, float_fmt))
    print("from 2 to 1 :", format(solution21, float_fmt))

print("adaptive quadrature")
do_view_factor_calc(configured_adaptive_triangle_view_factor)
print()

print("tensor product quadrature")
do_view_factor_calc(tensor_triangle_view_factor)
print()

print("symmetric quadrature")
do_view_factor_calc(symmetric_triangle_view_factor)
