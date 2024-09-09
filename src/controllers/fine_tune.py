import json
import os
from datetime import datetime
from logging import getLogger
from typing import Optional

from fastapi import APIRouter, File, UploadFile, WebSocket, WebSocketDisconnect, Request

from src.services.fine_tune import fine_tune, fine_tune_pdf

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


@router.post("/upload")
async def upload_file(file: UploadFile = File(...), dataset_name: Optional[str] = None):
    filename: str = dataset_name or file.filename.replace(" ", "_")

    # Check if file already exists
    pdf_file_path: str = f"{os.getcwd()}/pdfs/{filename}"
    if os.path.exists(pdf_file_path):
        return {"status_code": 404, "message": f"PDF already exists: {filename}"}

    with open(pdf_file_path, "wb") as f:
        f.write(await file.read())

    await fine_tune_pdf(pdf_file_path)

    return {"message": f"PDF uploaded successfully: {filename}"}


@router.get("/result/{dataset_name}")
async def get_dataset(request: Request, dataset_name: str):
    dataset_file_path: str = f"{os.getcwd()}/results/{dataset_name}"
    with open(dataset_file_path, "r") as f:
        dataset = json.load(f)
    return dataset
