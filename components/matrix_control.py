"""Sets up the matrix and canvas
"""
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from components.utils import get_config

def set_up_matrix():
    """Sets up the matrix and canvas

    Returns:
        tuple: matrix, canvas
    """
    options = RGBMatrixOptions()
    options.brightness = get_config('Hardware', 'brightness')
    options.cols = get_config('Hardware', 'pixel_width')
    options.gpio_slowdown = get_config('Hardware', 'gpio_slowdown')
    options.hardware_mapping = get_config('Hardware', 'hardware_mapping')
    options.rows = get_config('Hardware', 'pixel_height')

    matrix = RGBMatrix(options=options)
    canvas = matrix.CreateFrameCanvas()

    return matrix, canvas
