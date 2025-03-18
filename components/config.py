"""Loads the values in config.ini into config_dict
"""
import configparser

config = configparser.ConfigParser()
config.read('./config.ini')

config_dict = {}
for section in config.sections():
    config_dict[section] = {}
    for key in config[section]:
        if config[section][key].isdigit():
            config_dict[section][key] = int(config[section][key])
        else:
            try:
                config_dict[section][key]  = float(config[section][key])
            except ValueError:
                config_dict[section][key] = config[section][key]
