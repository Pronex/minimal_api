#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
minimal_api - rt_root.py
Author: pronex
"""

from typing import Any

from fastapi import APIRouter, status

# default route options for routes in this file
router = APIRouter(tags=['general'])


# routes
@router.get("/", status_code=status.HTTP_200_OK, summary="Liveness probe")
async def root() -> Any:
    """
    Root route and liveness probe.

    Returns:
        Any: json / dict with liveness info.
    """
    return {'status': 'alive'}