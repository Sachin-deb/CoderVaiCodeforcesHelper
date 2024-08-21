# app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import leaderboard, contest_info, auth, suggest_problem

def create_app() -> FastAPI:
    app = FastAPI()

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Replace with your frontend URL for production
        allow_credentials=True,
        allow_methods=["*"],  # Allow all HTTP methods
        allow_headers=["*"],  # Allow all headers
    )

    # Register the routers
    app.include_router(leaderboard.router)
    app.include_router(contest_info.router)
    app.include_router(auth.router)
    app.include_router(suggest_problem.router)
    
    return app

app = create_app()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
