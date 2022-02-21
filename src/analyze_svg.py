from typing import Union
from beziers import *
from series_math import*
from xml.dom import minidom
from svg.path import parse_path
from svg.path.path import *

#Read Svg File
class SvgIn:
    def __init__(self, svg_path:str, scale:float=1):
        doc = minidom.parse(svg_path)
        self.path_strings = [path.getAttribute('d') for path
                        in doc.getElementsByTagName('path')]
        doc.unlink()
        self.scale = scale

    def get_circumference(self):
        circumference = 0
        elements = {}
        for path_string in self.path_strings:
            path = parse_path(path_string)
            start = path[0].start * self.scale #center
            print(f"{path[0].start * self.scale}\n")
            for e in path:
                if isinstance(e, Line):
                    length = get_linear_length(start=e.start*self.scale, end=e.end*self.scale)
                    circumference += length
                    elements[length] = Line((e.start-start)*self.scale, (e.end-start)*self.scale)
                    #print(f"Line: {e}, Length: {length}px")

                elif isinstance(e, CubicBezier):
                    length = get_cubic_arc_length(P0=e.start*self.scale, P1=e.control1*self.scale, P2=e.control2*self.scale, P3=e.end*self.scale)
                    circumference += length
                    elements[length] = CubicBezier((e.start-start)*self.scale, (e.control1-start)*self.scale, (e.control2-start)*self.scale, (e.end-start)*self.scale)
                    #print(f"CubicBezier: {e}, Length: {length}px")

                elif isinstance(e, QuadraticBezier):
                    length = get_quadratic_arc_length(P0=e.start*self.scale, P1=e.control*self.scale, P2=e.end*self.scale)
                    circumference += length
                    elements[length] = QuadraticBezier((e.start-start)*self.scale, (e.control-start)*self.scale, (e.end-start)*self.scale)
                    #print(f"QuadraticBezier: {e}, Length: {length}px")

                #TODO
                elif isinstance(e, Arc):
                    pass
                
        self.circumference = circumference
        self.elements = elements

    def c2p(self):
        #Change length in elements into end proportion
        #i.e. 2 elements both with 50% circumference will end up be {0.5:ele1, 1.0:ele2}
        elements_proportion = {}
        #print(self.elements.keys())
        #print(list(self.elements))
        for index, key in enumerate(self.elements):
            new_key = key / self.circumference
            if index:
                #print(f"index: {index}, before: {list(elements_proportion)[index - 1]}")
                new_key += list(elements_proportion)[index - 1]    #key set
            elements_proportion[new_key] = self.elements[key]
        self.elements_proportion = elements_proportion
        #print(elements_proportion.keys())

    def export(self, _path:str, vectors:int, origin:tuple[float]=(0,-60,0)):
        self.coefficient = get_coefficients(self.elements_proportion, vectors)
        export_to_function_pack(origin, self.coefficient, path=_path)

