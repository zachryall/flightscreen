"""Sets the theme for the display
"""
from rgbmatrix import graphics
from components import config

font = graphics.Font()
font.LoadFont(config.config_dict['Display']['font_regular'])

font_small = graphics.Font()
font_small.LoadFont(config.config_dict['Display']['font_small'])
