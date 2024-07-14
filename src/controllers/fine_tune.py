import json
import os
from datetime import datetime
from logging import getLogger

from fastapi import APIRouter, WebSocket, WebSocketDisconnect, Request

from src.services.fine_tune import fine_tune

router = APIRouter()
logger = getLogger()


@router.websocket("/ws/upload")
async def websocket_upload(websocket: WebSocket):
    await websocket.accept()
    try:
        data = await websocket.receive_json()
        file_name: str = f"{data.get("dataset_name", "dataset")}{datetime.now().strftime('%Y%m%d%H%M%S')}.json"
        dataset: dict = data.get("dataset")

        dataset_file_path: str = f"{os.getcwd()}/datasets/{file_name}"
        with open(dataset_file_path, "w") as f:
            json.dump(dataset, f)
        await websocket.send_text("Dataset received. Starting fine-tuning...")
        await fine_tune(dataset_file_path)

        await websocket.send_text(f"Fine-tuning completed on file: {file_name}")
    except WebSocketDisconnect:
        print("Client disconnected")
    except Exception as e:
        await websocket.send_text(f"Error: {str(e)}")
    finally:
        await websocket.close()


@router.get("/result/{dataset_name}")
async def get_dataset(request: Request, dataset_name: str):
    dataset_file_path: str = f"{os.getcwd()}/results/{dataset_name}"
    with open(dataset_file_path, "r") as f:
        dataset = json.load(f)
    return dataset
