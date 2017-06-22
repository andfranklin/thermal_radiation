from scipy import integrate
import numpy as np

# scale = .1
#
# def func2(x0, x1, x2, x3, t0, t1):
#     return x0*x1*x3**2 + np.sin(x2) + 1 + (1 if x0+t1*x1-t0>0 else 0)
#
# def lim0(x1, x2, x3, t0, t1):
#     return [scale * (x1**2 + x2 + np.cos(x3)*t0*t1 + 1) - 1, scale * (x1**2 + x2 + np.cos(x3)*t0*t1 + 1) + 1]
#
# def lim1(x2, x3, t0, t1):
#     return [scale * (t0*x2 + t1*x3) - 1, scale * (t0*x2 + t1*x3) + 1]
#
# def lim2(x3, t0, t1):
#     return [scale * (x3 + t0**2*t1**3) - 1, scale * (x3 + t0**2*t1**3) + 1]
#
# def lim3(t0, t1):
#     return [scale * (t0+t1) - 1, scale * (t0+t1) + 1]
#
# def opts0(x1, x2, x3, t0, t1):
#     return {'points' : [t0 - t1*x1]}
#
# def opts1(x2, x3, t0, t1):
#     return {}
#
# def opts2(x3, t0, t1):
#     return {}
#
# def opts3(t0, t1):
#     return {}
#
# sol = integrate.nquad(func2, [lim0, lim1, lim2, lim3], args=(0,0), opts=[opts0, opts1, opts2, opts3])
# print(sol)
# (25.066666666666666, 2.7829590483937256e-13)

def func(from_xi, from_eta, to_xi, to_eta):
    return from_xi

def from_xi_constraint(from_eta, to_xi, to_eta):
    return [0.0, 1.0 - from_eta]

def from_eta_constraint(to_xi, to_eta):
    return [0.0, 1.0]

def to_xi_constraint(to_eta):
    return [0.0, 1.0 - to_eta]

def to_eta_constraint():
    return [0.0, 1.0]

sol = integrate.nquad(func, [from_xi_constraint, from_eta_constraint, to_xi_constraint, to_eta_constraint])
print(sol)
