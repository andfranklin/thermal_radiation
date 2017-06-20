from math import sqrt

def two_infintely_long_plates(w1, w2, d):
    """
    Calculates the view factor from plate 1 to plate 2 where both plates are
    infinitely long in one direction. The centerlines of the plates are
    connected by a perpendicular.

                                          plate 2
                              plate 1        _   ___
                           ___   _          | |   A
                            A   | |         | |   |
                            |   | |         | |   |
                            w1  | |<-- d -->| |   w2
                            |   | |         | |   |
                           _V_  |_|         | |   |
                                            |_|  _V_

    w1 : width of the first plate
    w2 : width of the second plate
    d : distance between the two plates
    """
    B = w1 / d
    C = w2 / d
    t1 = sqrt(((B + C)**2) + 4)
    t2 = sqrt(((C - B)**2) + 4)
    return (1.0 / (2.0 * B)) * (t1 - t2)
