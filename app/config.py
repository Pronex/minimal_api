"""
Provides configuration for the project. Loads environment variables.
Originally from: mxmo0rhuhn
"""

import inspect
import os
import sys

from typing import Any

import yaml

import structlog

# Bootstrapping problem - we hereby hardcode the default config file name and define that
# it needs to be located in the folder above this python file
CONFIG_FILE_NAME = "config.yml"
CONFIG_FILE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../", CONFIG_FILE_NAME)

_logger = structlog.get_logger()  # logging


class GlobalConfig():
    """
    All configuration for the project. You can simply add an attribute to this class and it will be
    looked for during initialization of this config. If you call the attribute something like "my_option"
    it will look inside the config yaml for "my_option" as well as for environment variables in the format
    "MY_OPTION".
    """
    uname: str = ''
    pword: str = ''

    port: int = 8080


def load_yaml_config_file() -> dict[str, Any]:
    """Loads a yaml from the CONFIG_FILE_PATH and ensures its type.
    Returns:
        dict[str, Any]: The content of the yaml.
    """
    if os.path.isfile(CONFIG_FILE_PATH):
        with open(CONFIG_FILE_PATH, 'r', encoding='utf-8') as yaml_file:
            type_enforcer: dict[str, Any] = yaml.safe_load(yaml_file)
            return type_enforcer
    else:
        _logger.warning("Can not find any config file at location", config_file_path=CONFIG_FILE_PATH)
        return {}


# Global config Singleton
GLOBAL_CONFIG = GlobalConfig()


def _str2bool(str_value: str | None) -> bool:
    """
    Helper function to cast a String to a boolean semantically.

    Args:
        str_value (str): A random string.

    Returns:
        bool: A boolean indicating if the string was something that is semantically "True"
    """
    if str_value:
        return str_value.lower() in ("yes", "true", "t", "1")
    return False


def initialize_global_config() -> None:
    """Initialize the global config from config file and the environment variables.
    Watch out: This function might exit if not all mandatory config options are set!
    """
    # get all attributes that matter in the global config
    config_variable_names: dict[str, type] = {
        a[0]: type(a[1])
        for a in inspect.getmembers(GlobalConfig, lambda a: not inspect.isroutine(a))
        if not a[0].startswith('__') and not a[0].endswith('__')
    }

    # load the default config
    default_config = load_yaml_config_file()
    for key, value in default_config.items():
        if key in config_variable_names.keys():
            if config_variable_names[key] is bool and isinstance(value, str):
                setattr(GLOBAL_CONFIG, key, _str2bool(value))
            else:
                setattr(GLOBAL_CONFIG, key, config_variable_names[key](value))

    missing: bool = False
    for item in config_variable_names.keys():
        # load all configs from environment variables
        if item.upper() in os.environ:
            if config_variable_names[item] is bool:
                setattr(GLOBAL_CONFIG, item, _str2bool(os.environ.get(item.upper())))
            else:
                setattr(GLOBAL_CONFIG, item, config_variable_names[item](os.environ.get(item.upper())))

        # ensure that every config item is defined
        if getattr(GLOBAL_CONFIG, item) == "":
            _logger.error("Can not find mandatory config option in the config file or the environment variables",
                          option=item)
            missing = True

    if missing:
        _logger.error("Mandatory config option missing - exiting")
        sys.exit(1)