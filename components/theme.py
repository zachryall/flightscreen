"""Sets the theme for the display
"""
from rgbmatrix import graphics
from components.utils import get_config

font = graphics.Font()
value = get_config('Theme', 'font_regular')
font.LoadFont(get_config('Theme', 'font_regular'))

font_small = graphics.Font()
font_small.LoadFont(get_config('Theme', 'font_small'))

colour_main = graphics.Color(0, 255, 0)
colour_accent = graphics.Color(255, 0, 255)