import asyncio
from logging import getLogger

from fastapi import APIRouter


router = APIRouter()
logger = getLogger()


@router.get("/health")
async def health_check():
    return {"status": "healthy"}
