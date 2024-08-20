from fastapi import FastAPI
from app.api import leaderboard

def create_app() -> FastAPI:
    app = FastAPI()

    # Register the routers
    app.include_router(leaderboard.router)

    return app

