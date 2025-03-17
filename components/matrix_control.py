from rgbmatrix import RGBMatrix, RGBMatrixOptions
import config

def setUpMatrix():
    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = config.PIXEL_HEIGHT
    options.cols = config.PIXEL_WIDTH
    options.chain_length = 1
    options.parallel = 1
    options.hardware_mapping = config.HARDWARE_MAPPING
    options.gpio_slowdown = config.GPIO_SLOWDOWN
    options.brightness = config.BRIGHTNESS

    # Initialize the matrix
    matrix = RGBMatrix(options=options)

    # Create a canvas
    canvas = matrix.CreateFrameCanvas()

    return matrix, canvas