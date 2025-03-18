import os
import pytest
from components import config

def test_font_regular_exists():
    assert os.path.exists(config.config_dict['Display']['font_regular'])
    assert os.path.isfile(config.config_dict['Display']['font_regular'])
def test_font_regular_small():
    assert os.path.exists(config.config_dict['Display']['font_small'])
    assert os.path.isfile(config.config_dict['Display']['font_small'])