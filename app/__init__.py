from fastapi import FastAPI
from app.api import leaderboard, contest_info, auth

def create_app() -> FastAPI:
    app = FastAPI()

    # Register the routers
    app.include_router(leaderboard.router)
    app.include_router(contest_info.router)
    app.include_router(auth.router)
    
    return app

