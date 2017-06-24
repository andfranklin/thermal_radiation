import pickle
import numpy as np
from time import time
from math import tan, radians
from thermal_radiation.quadrature_2d import TriangleTensorProductGaussLegendre2D, TriangleSymmetricalGauss2D
from thermal_radiation.geometry import Triangle, get_fixed_triangle_view_factor

tensor_quad = TriangleTensorProductGaussLegendre2D(20, 20)
tensor_triangle_view_factor = get_fixed_triangle_view_factor(tensor_quad)

def apprx_parallel_directly_opposed_triangles(normalized_distance, theta, use_adaptive=False):
    base = 1.0
    distance = base * normalized_distance
    height = tan(radians(theta)) * base

    triangle1 = Triangle(
        [0.0,  0.0, 0.0   ], # a
        [0.0,  0.0, height], # b
        [base, 0.0, 0.0   ]  # c
    )

    triangle2 = Triangle(
        [0.0,  distance, 0.0   ], # a
        [base, distance, 0.0   ], # b
        [0.0,  distance, height]  # c
    )

    if use_adaptive:
        return adaptive_triangle_view_factor(triangle1, triangle2)
    else:
        return tensor_triangle_view_factor(triangle1, triangle2)


def pickle_data(file_name, data):
    with open(file_name, mode="wb") as pckl_file:
        pickle.dump(data, pckl_file)

relative_distaces = np.linspace(0.1, 10.0, 50)
angle = 45.0

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

angle_posfix = f"{angle:2.0f}.pkl"
pickle_data("view_factors_" + angle_posfix, angle_view_factors)
pickle_data("times_" + angle_posfix, times)
pickle_data("relative_dists_" + angle_posfix, rds)
