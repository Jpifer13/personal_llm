import asyncio
from logging import getLogger

from fastapi import APIRouter, WebSocket

from src.services.generate import generate_text

# from src.lib.authorized_api_handler import authorized_api_handler

router = APIRouter()
logger = getLogger()


@router.websocket("/ws/run")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    prompt = await websocket.receive_text()
    generated_text = await generate_text(prompt)
    for char in generated_text:
        await websocket.send_text(char)
        await asyncio.sleep(0.01)  # Simulate typing delay
    await websocket.close()
