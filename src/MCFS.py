from analyze_svg import SvgIn

svg_obj = SvgIn("../TestSVGs/He.svg", 0.1)
if svg_obj.error:
    print("FileNotFound")
else:
    svg_obj.get_circumference()
    print(svg_obj.circumference)
    svg_obj.c2p()
    svg_obj.export(r"C:\Users\FedeleWu\AppData\Local\Packages\Microsoft.MinecraftUWP_8wekyb3d8bbwe\LocalState\games\com.mojang\minecraftWorlds\43cMYrbQAQA=", 301)