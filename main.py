from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import requests
import time

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


@app.get("/getcontestlistforuser/{handles}/{how_many_contest_result}")
def read_contest_list(handles: str, how_many_contest_result: int):
    api_url = "https://codeforces.com/api/contest.list?gym=false"
    
    response = requests.get(api_url)
    response.raise_for_status()  # Raises an HTTPError for bad responses (4xx and 5xx)

    contests = response.json().get('result', [])
    
    current_time = int(time.time())  # Get the current system time in seconds

    contest_list = []
    for contest in contests:
        start_time_seconds = contest.get('startTimeSeconds', 0)
        if start_time_seconds < current_time:
            contest_list.append(contest['id'])
            
    contest_list = contest_list[:how_many_contest_result]

    fetch_user_info_url = f"https://codeforces.com/api/user.info?handles={handles}&checkHistoricHandles=false"
    response = requests.get(fetch_user_info_url)
    response.raise_for_status()

    user_infos = response.json().get('result', [])
    contest_standing = []

    for contest in contest_list:
        fetch_contest_info = f"https://codeforces.com/api/contest.standings?contestId={contest}&handles={handles}"
        response = requests.get(fetch_contest_info)
        response.raise_for_status()
        response_json = response.json()
        rows = response_json.get('result', {}).get('rows', [])
        
        # Debug print to check API response
        print(f"Contest ID: {contest}, Response JSON: {response_json}")

        for row in rows:
            contest_standing.append({
                'contestId': contest,
                'handle': row['party']['members'][0]['handle'],
                'rank': row['rank']
            })
    
    # Debug print to check contest_standing data
    print(f"Contest Standing Data: {contest_standing}")
    
    response_user_list = []
    for user_info in user_infos:
        contest_standing_for_user = []
        for contest in contest_list:
            flag = 0
            for standing in contest_standing:
                # Debug print to check standing data
                print(f"Checking Standing: {standing}, User Info: {user_info}")
                
                if standing['handle'] == user_info['handle'] and standing['contestId'] == contest:
                    contest_standing_for_user.append(standing['rank'])
                    flag = 1
                    break
            if flag == 0:
                contest_standing_for_user.append(-1)
        response_user_list.append({
            'handle': user_info['handle'],
            'rating': user_info['rating'],
            'max_rating': user_info['maxRating'],
            'contribution': user_info['contribution'],
            'rank': user_info['rank'],
            'contest_rank': contest_standing_for_user
        })
    
    return response_user_list





