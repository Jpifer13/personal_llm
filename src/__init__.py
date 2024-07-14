from logging import Logger
import os
from typing import TYPE_CHECKING

from src.lib.constants import ORIGINS
from src.lib.loggers import get_module_logger

if TYPE_CHECKING:
    from src.config import Config

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles


class Application:
    def __init__(self, config: "Config"):
        self.logger: Logger = config.LOGGER if config.LOGGER else get_module_logger()
        self.logger.setLevel(config.LOG_LEVEL)
        self._app = FastAPI(
            title="LLM",
            openapi_url="/openapi.json",
            root_path="/dev",
            version="0.0.1",
        )

        # Add CORS headers
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=ORIGINS,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

        # Connect routers to the application
        self._connect_routers()

        # Fallback to the UI
        # if os.path.exists(f"{os.getcwd()}/src/static"):
        #     self._app.mount(
        #         "/static",
        #         StaticFiles(directory=f"{os.getcwd()}/src/static"),
        #         name="static"
        #     )

        # Fallback to the UI
        if os.path.exists("/tmp/static"):
            self._app.mount(
                "/",
                StaticFiles(directory="/tmp/static", html=True),
                name="static"
            )

    @property
    def app(self) -> FastAPI:
        return self._app

    def _connect_routers(self) -> None:
        import src.controllers as controllers

        routers = [
            controllers.fine_tune.router,
            controllers.health.router,
            controllers.websocket.router,
        ]

        for router in routers:
            self._app.include_router(router)
