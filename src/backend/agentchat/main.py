import logging
import os
import warnings
from contextlib import asynccontextmanager
from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

from agentchat.middleware.trace_id_middleware import TraceIDMiddleware
from agentchat.middleware.white_list_middleware import WhitelistMiddleware
from agentchat.settings import initialize_app_settings
from agentchat.settings import app_settings

warnings.filterwarnings("ignore")
logging.getLogger("chromadb").setLevel(logging.WARNING)


async def register_router(app: FastAPI):
    from agentchat.api.router import router

    app.include_router(router)

    if app_settings.storage and app_settings.storage.mode == "local":
        from agentchat.services.storage import storage_client
        storage_dir = getattr(storage_client, 'storage_dir', os.path.abspath('./storage'))
        os.makedirs(storage_dir, exist_ok=True)
        app.mount("/local_storage", StaticFiles(directory=storage_dir), name="local_storage")

    @app.get("/health")
    def check_health():
        return {'status': 'OK'}


def register_middleware(app: FastAPI):
    origins = [
        '*',
    ]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=False,
        allow_methods=['*'],
        allow_headers=['*'],
    )

    app.add_middleware(TraceIDMiddleware)
    app.add_middleware(WhitelistMiddleware)

    return app


async def init_config():
    await initialize_app_settings()

    from agentchat.database.init_data import (
        init_database,
        init_default_agent,
        update_system_mcp_server,
        upload_user_avatars_storage
    )
    await init_database()
    await init_default_agent()
    await update_system_mcp_server()
    await upload_user_avatars_storage()


def print_logo():
    from pyfiglet import Figlet

    f = Figlet(font="slant")
    print(f.renderText("WanxAgent"))


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_config()
    await register_router(app)
    print_logo()
    yield


def create_app():
    app = FastAPI(
        title=app_settings.server.get("project_name", "WanxAgent"),
        version=app_settings.server.get("version", "v2.4.0"),
        lifespan=lifespan
    )

    app = register_middleware(app)

    return app


app = create_app()


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("agentchat.main:app", host="0.0.0.0", port=7860)
