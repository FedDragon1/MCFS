from svg.path.path import *

def get_quadratic_coordinate_with_time(t:float, /, *, p0:complex, p1:complex, p2:complex):
    if t < 0 or t > 1:
        return
    points = [p0, p1, p2]
    polynomials = [eval("(1-t)**2"), eval("2*t*(1-t)"), eval("t**2")]
    return sum([prod * points[index] for index, prod in enumerate(polynomials)])

def get_quadratic_arc_length(n:int = 40, /, *, P0:complex, P1:complex, P2:complex):
    """
    Get the arc length of a quadratc bezier curve
    -------------
    Formelae: (i=1 Σ n) ||f(i/n) - f((i-1)/n)||

    """
    if n < 1:
        return
    return sum([abs(get_quadratic_coordinate_with_time((side_count + 1) / n, p0=P0, p1=P1, p2=P2) - get_quadratic_coordinate_with_time(side_count / n, p0=P0, p1=P1, p2=P2)) for side_count in range(n)])


def get_cubic_coordinate_with_time(t:float, /, *, p0:complex, p1:complex, p2:complex, p3:complex):
    if t < 0 or t > 1:
        return
    points = [p0, p1, p2, p3]
    polynomials = [eval("-t**3 + 3*t**2 -3*t + 1"), eval("3*t**3 - 6*t**2 + 3*t"), eval("-3*t**3 + 3*t**2"), eval("t**3")]
    return sum([prod * points[index] for index, prod in enumerate(polynomials)])

def get_cubic_arc_length(n:int = 40, /, *, P0:complex, P1:complex, P2:complex, P3:complex):
    """
    Get the arc length of a cubic bezier curve
    -------------
    (i=1 Σ n) ||f(i/n) - f((i-1)/n)||
    """
    if n < 1:
        return
    return sum([abs(get_cubic_coordinate_with_time((side_count + 1) / n, p0=P0, p1=P1, p2=P2, p3=P3) - get_cubic_coordinate_with_time(side_count / n, p0=P0, p1=P1, p2=P2, p3=P3)) for side_count in range(n)])

# "linear" beziers
def get_linear_coordinate_with_time(t:float, /, *, start:complex, end:complex):
    if t < 0 or t > 1:
        return
    return (1-t)*start + t*end

def get_linear_length(*, start:complex, end:complex):
    return abs(end - start)

def point_from_proportion(t:float, elements:dict):
    if t < 0 or t > 1:
        return
    for index, key in enumerate(elements):
        if key >= t:
            #The point is on this element
            element = elements[key]
            element_end = list(elements)[index]
            if index:
                element_start = list(elements)[index-1]
            else:
                element_start = 0
            break
    #find proportion of the point on element
    element_end -= element_start
    t -= element_start
    alpha = t / element_end
    #different kind of elements
    if isinstance(element, Line):
        return get_linear_coordinate_with_time(alpha, start=element.start, end=element.end)
    elif isinstance(element, QuadraticBezier):
        return get_quadratic_coordinate_with_time(alpha, p0=element.start, p1=element.control, p2=element.end)
    elif isinstance(element, CubicBezier):
        return get_cubic_coordinate_with_time(alpha, p0=element.start, p1=element.control1, p2=element.control2, p3=element.end)
    else:
        raise NotImplementedError(f"Element type \"{type(element)}\" is not implemented yet")
    