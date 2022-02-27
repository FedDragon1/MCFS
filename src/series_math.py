# !/usr/bin/python
# -*- coding: UTF-8 -*-
import numpy as np
import sys
import shutil
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
    result = {key:result[key] for key in sorted(result.keys(), key=abs)}
    #print(result.items())
    return result

def export_to_function_pack(origin:tuple, coefficients:dict, *, particle:str = "minecraft:endRod", path:str = ".", name:str = "Demo"):
    if len(origin) != 3:
        return

    #real freq = freq / 10, so it won't be dizzy
    #minecraft RoX = clockwise, so frep -1 would be ^^^r~0.5555555
    init_func = []
    play_func = []
    reset_func = ["kill @e[name=origin]"]
    init_func.append(f"summon armor_stand \"origin\" {origin[0]} {origin[1]} {origin[2]}")
    for freq, coefficient in coefficients.items():
        if freq == 0:
            previous_name = "origin"
        else:
            #freq sequence: [0, -1, 1, -2, 2...]
            previous_name = str(-freq) if abs(freq) == freq else str(abs(freq)-1)

        try:
            radius = radius_next
        except:
            radius = 0

        radius_next = abs(coefficient)
        angle = np.angle(coefficient, deg=True)
        
        init_func.append(f"summon armor_stand \"{freq}\" {origin[0]} {origin[1]} {origin[2]}")
        init_func.append(f"execute @e[name=\"{previous_name}\"] ^^^ tp @e[name=\"{freq}\"] ^^^{radius} ~{angle}")
        play_func.append(f"execute @e[name=\"{previous_name}\"] ^^^ tp @e[name=\"{freq}\"] ^^^{radius}")
        play_func.append(f"execute @e[name=\"{freq}\"] ~~~ tp @s ~~~ ~{-0.555555 * freq}")
        reset_func.append(f"kill @e[name=\"{freq}\"]")

    #place particle down
    play_func.append(f"execute @e[name=\"{freq}\"] ^^^ particle {particle} ^^2^{radius_next}")

    shutil.copytree("..\\lib\\Behavior", f"{path}\\behavior_packs", dirs_exist_ok=True)
    shutil.copytree("..\\lib\\Resource", f"{path}\\resource_packs", dirs_exist_ok=True)

    with open(fr"{path}\behavior_packs\FunctionByMCFS\functions\init.mcfunction", "w") as file:
        for func in init_func:
            file.write(func + '\n')

    with open(fr"{path}\behavior_packs\FunctionByMCFS\functions\play.mcfunction", "w") as file:
        for func in play_func:
            file.write(func + '\n') 

    with open(fr"{path}\behavior_packs\FunctionByMCFS\functions\reset.mcfunction", "w") as file:
        for func in reset_func:
            file.write(func + '\n') 
    