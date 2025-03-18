"""Sets up the matrix and canvas
"""
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from components import config

def set_up_matrix():
    """Sets up the matrix and canvas

    Returns:
        tuple: matrix, canvas
    """
    options = RGBMatrixOptions()
    options.brightness = config.config_dict['Hardware']['brightness']
    options.chain_length = 1
    options.cols = config.config_dict['Hardware']['pixel_width']
    options.gpio_slowdown = config.config_dict['Hardware']['gpio_slowdown']
    options.hardware_mapping = config.config_dict['Hardware']['hardware_mapping']
    options.parallel = 1
    options.rows = config.config_dict['Hardware']['pixel_height']

    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()

    return matrix, canvas
