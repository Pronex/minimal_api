#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
minimal_api
Author: pronex
"""

import secrets

import structlog

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

from app.config import GLOBAL_CONFIG

# HTTP Basic Auth
security = HTTPBasic()  # security scheme HTTPBasic
_logger = structlog.get_logger()  # logging


# credentials helper
def verify_creds(credentials: HTTPBasicCredentials = Depends(security)) -> str:
    """
    Helper to check HTTP Basic Auth credentials.

    Args:
        credentials (HTTPBasicCredentials, optional): Set of HTTP Basic creds. Defaults to Depends(security).

    Raises:
        HTTPException: raised if credentials are invalid.

    Returns:
        str: username of the given credentials.
    """
    # implemented according to doc: https://fastapi.tiangolo.com/advanced/security/http-basic-auth/
    correct_username = secrets.compare_digest(credentials.username, GLOBAL_CONFIG.uname)
    correct_password = secrets.compare_digest(credentials.password, GLOBAL_CONFIG.pword)

    if not (correct_username and correct_password):
        _logger.warning('Invalid credentials.')
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail="Incorrect credentials provided.",
                            headers={"WWW-Authenticate": "Basic"})
    return credentials.username
