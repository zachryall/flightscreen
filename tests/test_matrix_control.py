import pytest
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from components import config
from components.matrix_control import set_up_matrix

def test_set_up_matrix_options():
    matrix, canvas, options = set_up_matrix()

    assert options.brightness == config.config_dict['Hardware']['brightness']
    assert options.cols == config.config_dict['Hardware']['pixel_width']
    assert options.gpio_slowdown == config.config_dict['Hardware']['gpio_slowdown']
    assert options.hardware_mapping.decode('utf-8') == config.config_dict['Hardware']['hardware_mapping']
    assert options.rows == config.config_dict['Hardware']['pixel_height']
    assert options.chain_length == 1
    assert options.parallel == 1

def test_set_up_matrix_creation():
    matrix, canvas, options = set_up_matrix()

    assert isinstance(matrix, RGBMatrix)
    assert canvas is not None

def test_set_up_matrix_config_keys_exists():
    assert 'Hardware' in config.config_dict
    assert 'brightness' in config.config_dict['Hardware']
    assert 'pixel_width' in config.config_dict['Hardware']
    assert 'gpio_slowdown' in config.config_dict['Hardware']
    assert 'hardware_mapping' in config.config_dict['Hardware']
    assert 'pixel_height' in config.config_dict['Hardware']

def test_set_up_matrix_config_keys_types():
    assert 'Hardware' in config.config_dict
    assert isinstance(config.config_dict['Hardware']['pixel_width'], int)
    assert isinstance(config.config_dict['Hardware']['pixel_height'], int)
    assert isinstance(config.config_dict['Hardware']['brightness'], int)
    assert isinstance(config.config_dict['Hardware']['gpio_slowdown'], int)
    assert isinstance(config.config_dict['Hardware']['hardware_mapping'], str)

def test_set_up_matrix_config_keys_valid():
    assert 'Hardware' in config.config_dict
    assert config.config_dict['Hardware']['pixel_width'] % 16 == 0
    assert config.config_dict['Hardware']['pixel_height'] % 16 == 0
    assert 1 <= config.config_dict['Hardware']['brightness'] <= 100
    assert config.config_dict['Hardware']['hardware_mapping'] == 'adafruit-hat'