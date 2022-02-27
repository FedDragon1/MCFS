# !/usr/bin/python
# -*- coding: UTF-8 -*-
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from os.path import isfile, isdir
from analyze_svg import SvgIn

class MainLayout(BoxLayout):
    def generate(self, widget, svg, world, factor, count, origin):
        widget.background_color = (.3, .9, .2)
        self.svg_path_validate(svg, True)
        self.world_path_validate(world, True)
        self.float_validate(factor)
        self.int_validate(count)
        self.tuple_validate(origin)

        print(svg.background_color, world.background_color, factor.background_color, count.background_color)
        if svg.background_color == [0.6, 1, 0.6, 1.0] and world.background_color == [0.6, 1, 0.6, 1.0] and factor.background_color == [0.6, 1, 0.6, 1.0] and count.background_color == [0.6, 1, 0.6, 1.0] and origin.background_color == [0.6, 1, 0.6, 1.0]:
            print(str(svg.text.replace("\\", "/")))
            obj = SvgIn(svg.text.replace("\\", "/"), float(factor.text))
            obj.get_circumference()
            obj.c2p()
            obj.export(world.text.replace("\\", "/"), int(count.text))
            widget.text = "生成成功！（点击再次生成）"
        else:
            widget.text = "生成失败！（检查红色区域）"

    def svg_path_validate(self, widget, final=False):
        raw_text = widget.text.replace("\\", "/")
        if raw_text:
            if isfile(raw_text):
                widget.background_color = (0.6, 1, 0.6)
            else:
                widget.background_color = (1, 0.6, 0.6)
        else:
            if final:
                widget.background_color = (1, 0.6, 0.6)
                return
            widget.background_color = (.8, .8, .8)
    
    def world_path_validate(self, widget, final=False):
        raw_text = widget.text.replace("\\", "/")
        if raw_text:
            if isdir(raw_text):
                widget.background_color = (0.6, 1, 0.6)
            else:
                widget.background_color = (1, 0.6, 0.6)
        else:
            if final:
                widget.background_color = (1, 0.6, 0.6)
                return
            widget.background_color = (.8, .8, .8)

    def float_validate(self, widget):
        try:
            1 / float(widget.text) #incase 0
        except:
            widget.background_color = (1, 0.6, 0.6)
        else:
            widget.background_color = (0.6, 1, 0.6)

    def int_validate(self, widget):
        try:
            if int(widget.text) <= 0: raise ValueError()
        except:
            widget.background_color = (1, 0.6, 0.6)
        else:
            widget.background_color = (0.6, 1, 0.6)

    def tuple_validate(self, widget):
        coor = widget.text.replace(" ", "").split(",")
        print(coor)
        if len(coor) == 3:
            try:
                float_coor = [float(x) for x in coor]
                if float_coor[1] > -64:
                    widget.background_color = (0.6, 1, 0.6)
                else:
                    widget.background_color = (1, 0.6, 0.6)
            except:
                widget.background_color = (1, 0.6, 0.6)
        else:
            widget.background_color = (1, 0.6, 0.6)
    
class MCfsApp(App):
    def build(self):
        self.icon = "../lib/images/icon.png"

MCfsApp().run()