from xml.dom import minidom
from svg.path import parse_path
from svg.path.path import *
import numpy as np

doc = minidom.parse("../TestSVGs/EighthNote.svg")
path_strings = [path.getAttribute('d') for path
                in doc.getElementsByTagName('path')]
doc.unlink()

for path_string in path_strings:
    path = parse_path(path_string)
    print(path)
    for e in path:
        if isinstance(e, Line):
            print(f"Line: {e}")
        elif isinstance(e, CubicBezier):
            print(f"CubicBezier: {e}")
        elif isinstance(e, QuadraticBezier):
            pass
        elif isinstance(e, Arc):
            pass