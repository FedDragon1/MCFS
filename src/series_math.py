from unittest import result
import numpy as np
import sys
from beziers import *
from math import pi

np.set_printoptions(threshold=sys.maxsize)

#partial code from https://github.com/3b1b/videos/blob/master/_2019/diffyq/part2/fourier_series.py
def get_coefficients(elements:dict, vector_count:int, samples:int = 10000):
    if samples < 0 or vector_count < 0:
        return

    dt = 1 / samples
    time_samples = np.arange(0, 1, dt)
    path_samples = np.array([point_from_proportion(t, elements) for t in time_samples])

    freqs = [x - int(vector_count / 2) for x in range(vector_count)]
    result = {}
    for freq in freqs:
        #Integral of exp(-2pi * i * n * t) * f(t) from 0 to 1
        riemann_sum = sum([np.exp(-2 * pi * 1j * freq * time_sample) * path_sample for time_sample, path_sample in zip(time_samples, path_samples)]) * dt
        result[freq] = riemann_sum
    print(result.items())
    result = {key:result[key] for key in sorted(result.keys(), key=abs)}
    return result

def export_to_function_pack(origin:tuple, scale:float, constants:dict):
    for freq, constant in constants.items():
        pass