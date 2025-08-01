"""Sets the theme for the display
"""
from rgbmatrix import graphics
from components.utils import get_config

font = graphics.Font()
font.LoadFont(get_config('Theme', 'font_regular'))

font_small = graphics.Font()
font_small.LoadFont(get_config('Theme', 'font_small'))

font_overflow = graphics.Font()
font_overflow.LoadFont(get_config('Theme', 'font_overflow'))

colour_main = graphics.Color(
    get_config('Theme', 'colour_main_r'),
    get_config('Theme', 'colour_main_g'),
    get_config('Theme', 'colour_main_b')
)

colour_accent = graphics.Color(
    get_config('Theme', 'colour_accent_r'), 
    get_config('Theme', 'colour_accent_g'), 
    get_config('Theme', 'colour_accent_b')
)
