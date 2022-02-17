from beziers import *
from series_math import*
from xml.dom import minidom
from svg.path import parse_path
from svg.path.path import *
import os

#Read Svg File
doc = minidom.parse("../TestSVGs/EighthNote.svg")
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()

#Anylize paths
circumference = 0
elements = {}
for path_string in path_strings:
    path = parse_path(path_string)
    print(f"{path}\n")
    for e in path:
        if isinstance(e, Line):
            length = get_linear_length(start=e.start, end=e.end)
            circumference += length
            elements[length] = e
            print(f"Line: {e}, Length: {length}px")

        elif isinstance(e, CubicBezier):
            length = get_cubic_arc_length(P0=e.start, P1=e.control1, P2=e.control2, P3=e.end)
            circumference += length
            elements[length] = e
            print(f"CubicBezier: {e}, Length: {length}px")

        elif isinstance(e, QuadraticBezier):
            length = get_quadratic_arc_length(P0=e.start, P1=e.control, P2=e.end)
            circumference += length
            elements[length] = e
            print(f"CubicBezier: {e}, Length: {length}px")

        #TODO
        elif isinstance(e, Arc):
            pass

print()
print(circumference)

#Change length in elements into end proportion
#i.e. 2 elements both with 50% circumference will end up be {0.5:ele1, 1.0:ele2}
elements_proportion = {}
print(elements.keys())
print(list(elements))
for index, key in enumerate(elements):
    new_key = key / circumference
    if index:
        print(f"index: {index}, before: {list(elements_proportion)[index - 1]}")
        new_key += list(elements_proportion)[index - 1]    #key set
    elements_proportion[new_key] = elements[key]
del elements
print(elements_proportion.keys())

coefficients = get_coefficients(elements_proportion, 101)
export_to_function_pack((0,-60,0), 1, coefficients, path="C:\\Users\\FedeleWu\\AppData\\Local\\Packages\\Microsoft.MinecraftUWP_8wekyb3d8bbwe\\LocalState\\games\\com.mojang\\minecraftWorlds\\43cMYrbQAQA=")