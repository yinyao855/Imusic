import os.path

from colorthief import ColorThief


def rgb_to_css(rgb):
    return f'rgb({rgb[0]}, {rgb[1]}, {rgb[2]})'


def css_generate(image_path):
    # print(image_path)
    if not os.path.exists(image_path):
        return None
    color_thief = ColorThief(image_path)
    dominant_color = color_thief.get_color(quality=10)
    palette = color_thief.get_palette(color_count=3, quality=10)

    color1_css = rgb_to_css(palette[0])
    color2_css = rgb_to_css(palette[1])
    color3_css = rgb_to_css(palette[2])
    dominant_color_css = rgb_to_css(dominant_color)

    background = f'background: {dominant_color_css};'
    gradient = f'background: linear-gradient(135deg, {color1_css}, {color2_css});'

    return background + gradient
