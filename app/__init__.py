from fastapi import FastAPI
from app.api import leaderboard
from app.api import contest_info

def create_app() -> FastAPI:
    app = FastAPI()

    # Register the routers
    app.include_router(leaderboard.router)
    app.include_router(contest_info.router)
    
    return app

