from sympy.integrals.quadrature import gauss_legendre

PRECISION = 20

def get_gauss_legendre_pairs(order):
    qps, weights = gauss_legendre(order, PRECISION)
    apprx_qps = [float(qp) for qp in qps]
    apprx_weights = [float(weight) for weight in weights]
    return apprx_qps, apprx_weights


class Quadrature:
    def compute(self, func):
        total = 0.0
        for qp, weight in zip(self.qps, self.weights):
            total += weight * func(*qp)
        return total


class GaussLegendre1D(Quadrature):
    def __init__(self, n_qps):
        qps, weights = get_gauss_legendre_pairs(n_qps)
        self.qps = [(qp,) for qp in qps]
        self.weights = weights
        self.max_poly_order = (2 * len(self.qps)) - 1


if __name__ == '__main__':
    gl2 = GaussLegendre1D(2)
    def test_function_int(func):
        print("Around Origin  :", gl2.compute(func))

    print("Line")
    test_function_int(lambda x : x)
    print()

    print("Quad")
    test_function_int(lambda x : x * x)
    print()

    print("Cube")
    test_function_int(lambda x : x * x * x)
    print()

    print("Quart") # 2nd order GLQ is not exact
    test_function_int(lambda x : x * x * x * x)
