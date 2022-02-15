import numpy as np

def get_cubic_coordinate_with_time(t:float, /, *, p0:complex, p1:complex, p2:complex, p3:complex):
    if t < 0 or t > 1:
        raise ValueError(f"\"t\" value {t} is not in range [0, 1]")

    points = [p0, p1, p2, p3]
    polynomials = [eval("-t**3 + 3*t**2 -3*t + 1"), eval("3*t**3 - 6*t**2 + 3*t"), eval("-3*t**3 + 3*t**2"), eval("t**3")]
    return sum([prod * points[index] for index, prod in enumerate(polynomials)])

def get_cubic_arc_length(n:int = 40, /, *, P0:complex, P1:complex, P2:complex, P3:complex):
    """
    Get the arc length of a cubic bezier curve
    (i=1 Σ n) ||f(i/n) - f((i-1)/n)||
    """
    return sum([abs(get_cubic_coordinate_with_time((side_count + 1), p0=P0, p1=P1, p2=P2, p3=P3) - get_cubic_coordinate_with_time((side_count), p0=P0, p1=P1, p2=P2, p3=P3)) for side_count in range(n)])

