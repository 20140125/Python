#!/usr/bin/python3

from fastapi import APIRouter

from app.routers.v1 import auth, systemLog, users, file, image

router = APIRouter()

router.include_router(auth.router, tags=['Authentication'])
router.include_router(systemLog.router, tags=['Log'])
router.include_router(users.router, tags=['Users'])
router.include_router(file.router, tags=['File'])
router.include_router(image.router, tags=['Image'])
