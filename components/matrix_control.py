import configparser
from rgbmatrix import RGBMatrix, RGBMatrixOptions

config = configparser.ConfigParser()
config.read('./config.ini')

def set_up_matrix():
    options = RGBMatrixOptions()
    options.brightness = config.getint("Hardware", "brightness")
    options.chain_length = 1
    options.cols = config.getint("Hardware", "pixel_width")
    options.gpio_slowdown = config.getint("Hardware", "gpio_slowdown")
    options.hardware_mapping = config.get("Hardware", "hardware_mapping")
    options.parallel = 1
    options.rows = config.getint("Hardware", "pixel_height")

    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()

    return matrix, canvas
