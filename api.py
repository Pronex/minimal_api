#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
minimal_api
Author: pronex
"""

import structlog

import uvicorn  # ASGI server
from fastapi import Depends, FastAPI

from app.config import initialize_global_config, GLOBAL_CONFIG

from app.utils import verify_creds
from app.routes import rt_root

_logger = structlog.get_logger()  # logging
initialize_global_config()  # initialize global config

# app description
DESC = "minimal_api - a minimalistic API template"

# create fastapi app
app = FastAPI(
    title="minmal_api",  # application title
    description=DESC,  # application description
    version="1.0.0",  # version numbering
    dependencies=[Depends(verify_creds)])  # defaults all routes to HTTP Basic Auth

# routes
app.include_router(rt_root.router)

# entrypoint (only used in debugging case, cf. README)
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=GLOBAL_CONFIG.port)