from kivy.properties import StringProperty
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.textinput import TextInput

class CustomTextInput(TextInput):
    pass

class MainLayout(BoxLayout):
    svg_path = StringProperty("")
    world_path = StringProperty("")
    scale_factor = StringProperty("1.0")
    vector_count = StringProperty("101")
    def generate(self):
        print("onclick")

class MCfsApp(App):
    pass

MCfsApp().run()