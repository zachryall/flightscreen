    """Sets the theme for the display
    """
import configparser
from rgbmatrix import graphics

config = configparser.ConfigParser()
config.read('./config.ini') #TODO remove

font = graphics.Font()
font.LoadFont(config.get("Display", "font_regular"))

font_small = graphics.Font()
font_small.LoadFont(config.get("Display", "font_small"))
