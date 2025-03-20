"""Sets the theme for the display
"""
from rgbmatrix import graphics
from components import config

font = graphics.Font()
font.LoadFont(config.config_dict['Theme']['font_regular'])

font_small = graphics.Font()
font_small.LoadFont(config.config_dict['Theme']['font_small'])

colour_main = graphics.Color(0, 255, 0)
colour_accent = graphics.Color(255, 0, 255)