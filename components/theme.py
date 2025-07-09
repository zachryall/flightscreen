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

main_r = get_config('Theme', 'colour_main_r')
main_g = get_config('Theme', 'colour_main_g')
main_b = get_config('Theme', 'colour_main_b')

accent_r = get_config('Theme', 'colour_accent_r')
accent_g = get_config('Theme', 'colour_accent_g')
accent_b = get_config('Theme', 'colour_accent_b')

colour_main = graphics.Color(main_r, main_g, main_b)
colour_accent = graphics.Color(accent_r, accent_g, accent_b)
