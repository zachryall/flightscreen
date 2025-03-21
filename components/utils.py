"""Collection of utilites
"""
import configparser
import functools

@functools.lru_cache(maxsize=128)
def get_config(section, key):
    """Gets the config from ini file, gets the default value if one is not available

    Args:
        section (str): Section that the key is under
        key (str): Key of the config item

    Returns:
        _type_: The key's value, or default value if one is not available
    """
    if not hasattr(get_config, "cache"):
        get_config.cache = {}

    cache_key = (section, key)

    if cache_key in get_config.cache:
        return get_config.cache[cache_key]

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

    get_config.cache[cache_key] = value
    return value
