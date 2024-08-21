import requests
import time
from fastapi import APIRouter

router = APIRouter()

@router.get("/contest-info")
def get_contest_info(how_many_contest_result: int = 10):
    """Fetches the list of past contests from Codeforces."""
    contest_list = fetch_contest_info_list(how_many_contest_result)
    return contest_list

def fetch_contest_info_list(how_many_contest_result: int):
    """Fetch contest information including id, name, start time, and duration."""
    api_url = "https://codeforces.com/api/contest.list?gym=false"
    response = requests.get(api_url)
    response.raise_for_status()

    contests = response.json().get('result', [])
    current_time = int(time.time())

    contest_list = [
        {
            'id': contest['id'],
            'name': contest['name'],
            'start_time': contest.get('startTimeSeconds', 0),
            'duration_seconds': contest['durationSeconds']
        }
        for contest in contests
        if contest.get('startTimeSeconds', 0) < current_time
    ]

    return contest_list[:how_many_contest_result]