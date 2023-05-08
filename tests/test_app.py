# -*- coding: utf-8 -*-
"""
minimal_api - test_app.py
Author: pronex
"""

import os
import sys

sys.path.append("..")  # adds higher directory to python modules path

import structlog

from config import initialize_global_config, GLOBAL_CONFIG

from random import randint

from fastapi.testclient import TestClient

from api import app

log = structlog.get_logger()  # logging
initialize_global_config()  # initialize global config

# check environment variables
log.debug("--------------------")
log.debug("ENVIRONMENT VARIABLES:")
for env in os.environ:
    log.debug(f"ENV: {env}={os.environ[env]}")

# check global config
log.debug(f"GLOBAL_CONFIG: {GLOBAL_CONFIG.__dict__}")

# create test client
client = TestClient(app)

# set authentication header
auth_header = (GLOBAL_CONFIG.uname, GLOBAL_CONFIG.pword)


# test routes
def test_root() -> None:
    """
    Test the root route.
    """
    response = client.get("/", auth=auth_header)
    assert response.status_code == 200
    assert response.json() == {"status": "alive"}


def test_unknown_route() -> None:
    """
    Test the unknown route.
    """
    response = client.get("/unknown")
    assert response.status_code == 404
    assert response.json() == {"detail": "Not Found"}


def test_unauthenticated_route() -> None:
    """
    Test the unauthenticated route.
    """
    response = client.get("/")
    assert response.status_code == 401
    assert response.json() == {"detail": "Not authenticated"}


# more cool test routes
