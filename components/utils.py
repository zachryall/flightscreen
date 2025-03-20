"""Collection of utilites
"""
import configparser
import logging


def get_config(section, key):

    config = configparser.ConfigParser()
    config.read('./config.ini')

    config_default = configparser.ConfigParser()
    config_default.read('./defaults.ini')

    default = config_default.get(section, key)
    
    if default.isdigit():
        try:
            value = config.getint(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = config_default.getint(section, key)
    elif isinstance(default, float):
        try:
            value = config.getfloat(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = config_default.getfloat(section, key)
    elif isinstance(default, bool):
        try:
            value = config.getboolean(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = config_default.getboolean(section, key)
    else:
        try:
            value = config.get(section, key)
        except (configparser.NoSectionError, configparser.NoOptionError):
            value = config_default.get(section, key)
    return value
