#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
minimal_api
Author: pronex
Load environment variables from config.yml file and run the app in a docker container
"""

import os
import sys
import structlog

from app.config import load_yaml_config_file

_logger = structlog.get_logger()  # logging

# load config.yml
cfg = load_yaml_config_file()

# implement --help flag
if "--help" in sys.argv:
    help_message = """
    Usage: python docker_run.py
    Build docker image and run the app in a docker container.
    Loads environment variables from config.yml file.
    """
    print(help_message)
    sys.exit(0)

# compose environment variables for docker run command
env_vars = " ".join([f"-e {name.upper()}={value}" for name, value in cfg.items()])
_logger.info(f"environment variables for docker run command: {env_vars}")

# build docker image
os.system("docker build -t minimal_api:latest .")

# remove docker container if it exists
os.system("docker rm -f minimal_api")

# run the app in docker container with env variables
os.system(f"docker run -it --name minimal_api -p {cfg['port']}:{cfg['port']} {env_vars} minimal_api:latest")
