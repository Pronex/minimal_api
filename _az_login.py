#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
minimal_api
Author: pronex
Login to Azure with service principal credentials from tf.env
"""

import os
import sys
import structlog

_logger = structlog.get_logger()  # logging

# path to tf.env
ENV_FILE = "tf.env"

# implement --help flag
if "--help" in sys.argv:
    help_message = """
    Usage: python az_login.py
    Login to Azure with service principal credentials from tf.env
    Expected environment variables:
        ARM_TENANT_ID
        ARM_CLIENT_ID
        ARM_CLIENT_SECRET
        ARM_SUBSCRIPTION_ID
    """
    print(help_message)
    sys.exit(0)

# read tf.env if it exists
if os.path.isfile(ENV_FILE):
    with open(ENV_FILE, "r") as f:
        for line in f.readlines():
            if line.startswith("export"):
                line = line.replace("export ", "")
            if "=" in line:
                var_name, var_value = line.split("=")
                os.environ[var_name] = var_value.strip()
else:
    _logger.warn("tf.env not found")
    sys.exit(1)


# check if environment variables are set
def check_env_var(var_name: str) -> None:
    if not os.getenv(var_name):
        _logger.error(f"{var_name} not set")
        sys.exit(1)


for var_name in ["ARM_SUBSCRIPTION_ID", "ARM_CLIENT_ID", "ARM_CLIENT_SECRET", "ARM_TENANT_ID"]:
    check_env_var(var_name)

# login to Azure
os.system("az login --service-principal -u $ARM_CLIENT_ID -p $ARM_CLIENT_SECRET --tenant $ARM_TENANT_ID")

# set subscription
os.system("az account set --subscription $ARM_SUBSCRIPTION_ID")

# get current subscription
os.system("az account show --query name")

# check if login was successful
if os.system("az account show") != 0:
    _logger.error("Login to Azure failed")
    sys.exit(1)

_logger.info("Login to Azure successful")
