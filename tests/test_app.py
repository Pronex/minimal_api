# -*- coding: utf-8 -*-
"""
minimal_api
Author: pronex
"""

import os
import sys

sys.path.append("..")  # adds higher directory to python modules path

import structlog

_logger = structlog.get_logger()  # logging

# check environment variables
_logger.debug("ENVIRONMENT VARIABLES:")
for env in os.environ:
    _logger.debug(f"ENV: {env}={os.environ[env]}")
_logger.debug("--------------------")

from app.config import initialize_global_config, GLOBAL_CONFIG

from fastapi.testclient import TestClient

from api import app

initialize_global_config()  # initialize global config

# check global config
_logger.debug(f"GLOBAL_CONFIG: {GLOBAL_CONFIG.__dict__}")

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
