from logging import getLogger

from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# from src.lib.authorized_api_handler import authorized_api_handler

router = APIRouter()
logger = getLogger(__name__)
templates = Jinja2Templates(directory="src/templates")


@router.get("/", response_class=HTMLResponse)
async def get_form(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
