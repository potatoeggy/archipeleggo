from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import islands

ORIGINS = ["*"]

ROUTERS = [
    islands.music.router
]

def create_app() -> FastAPI:

    app = FastAPI()
    app.add_middleware(
        CORSMiddleware,
        allow_origins=ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"]
    )

    for router in ROUTERS:
        app.include_router(router)

    return app