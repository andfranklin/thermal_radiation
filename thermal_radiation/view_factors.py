from math import sqrt, pi, atan, log

def two_infintely_long_plates(w1, w2, d):
    """
    Calculates the view factor from plate 1 to plate 2 where both plates are
    infinitely long in one direction. The centerlines of each plate are lined
    up.

                                          plate 2
                              plate 1        _   ___
                           ___   _          | |   A
                            A   | |         | |   |
                            |   | |         | |   |
                            w1  | |<-- d -->| |   w2
                            |   | |         | |   |
                           _V_  |_|         | |   |
                                            |_|  _V_

    Args:
        w1 (float): The width of the first plate.
        w2 (float): The width of the second plate.
        d (float): The distance between the two plates.

    Returns:
        float: The view factor from plate 1 to plate 2.
    """
    assert w1 > 0.0
    assert w2 > 0.0
    assert d > 0.0

    B = w1 / d
    C = w2 / d
    t1 = sqrt(((B + C)**2) + 4)
    t2 = sqrt(((C - B)**2) + 4)

    return (1.0 / (2.0 * B)) * (t1 - t2)

def two_coaxial_parallel_plates(l1, l2, d, apprx=False):
    """
    Calculates the view factor from plate 1 to plate 2 where both plates are
    finte and square. The centerlines of each plate are lined up.

                                                __
                                               / /|
                                              / / |
                                             / /  |
                                            /_/   |
                                 _          | |   |
                                | |         | |   |
                                | |         | |   |
                                | |<-- d -->| |   /
                                | |         | |  /
                                |_|         | | /
                                            |_|/

    Args:
        l1 (float): The side length of the first plate
        l2 (float): The side length of the second plate
        d (float): The distance between the two plates

    Returns:
        float: The view factor from plate 1 to plate 2.
    """
    assert l1 > 0.0
    assert l2 > 0.0
    assert d > 0.0

    A = l1 / d
    B = l2 / l1

    if apprx and A < 0.2:
        return ((A * B) ** 2) / pi

    else:
        X = A * (1 + B)
        Y = A * (1 - B)
        tmp = (A * A * (1 + (B * B))) + 2
        X4 = sqrt((X * X) + 4)
        Y4 = sqrt((Y * Y) + 4)

        denom = ((Y * Y) + 2) * ((X * X) + 2)
        f12  = log((tmp * tmp) / denom)
        f12 += Y4 * ((Y * atan(Y / Y4)) - (X * atan(X / Y4)))
        f12 += X4 * ((X * atan(X / X4)) - (Y * atan(Y / X4)))
        return f12 / (pi * A * A)


if __name__ == '__main__':
    view_factor = two_coaxial_parallel_plates(10.0, 10.0, 9.0, apprx=False)
    print(f"{view_factor:.40f}")
