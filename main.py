from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace with your frontend URL
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods
    allow_headers=["*"],  # Allow all headers
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/leaderboard/{contest_id}")
def read_leaderboard(contest_id: int):
    api_url = f"https://codeforces.com/api/contest.standings?contestId={contest_id}&from=1&count=5&showUnofficial=true"
    
    response = requests.get(api_url)
    
    if response.status_code == 200:
        json_response = []
        for row in response.json()['result']['rows']:
            json_response.append({
                'handle': row['party']['members'][0]['handle'],
                'points': row['points']
            })
        return json_response
    else:
        return {"error": f"Failed to retrieve data from Codeforces API. Status code: {response.status_code}"}
