from math import sqrt

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
