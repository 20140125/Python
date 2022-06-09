#!/usr/bin/python3

from fastapi import APIRouter

from app.routers import common
from app.routers import file

import app.routers.v1 as v1

router = APIRouter()

router.include_router(common.router, tags=['common'])
router.include_router(file.router, tags=['file'])
router.include_router(v1.router)
