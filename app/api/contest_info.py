import requests
import time
from fastapi import APIRouter

router = APIRouter()

@router.get("/contest-info")
def get_contest_info(how_many_contest_result: int = 10):
    api_url = "https://codeforces.com/api/contest.list?gym=false"
    response = requests.get(api_url)
    response.raise_for_status()

    contests = response.json().get('result', [])
    
    current_time = int(time.time())  # Get the current system time in seconds

    contest_list = []
    for contest in contests:
        start_time_seconds = contest.get('startTimeSeconds', 0)
        if start_time_seconds < current_time:
            contest_list.append({
                'id': contest['id'],
                'name': contest['name'],
                'start_time': start_time_seconds,
                'duration_seconds': contest['durationSeconds']
            })
    
    contest_list = contest_list[:how_many_contest_result]

    return contest_list

