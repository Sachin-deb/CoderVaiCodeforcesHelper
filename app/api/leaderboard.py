from fastapi import APIRouter
import requests
import time
import app.operations.user_repo as user_repo

router = APIRouter()

cached_response = False

@router.get("/")
def read_root():
    # user_repo.create_user("tourist", "tourist", "password", "email", "vjudge_handle") 
    return {"message": "Hello, World!"}

@router.get("/leaderboard")
def get_leaderboard():
    global cached_response
    if cached_response:
        return cached_response

    handles = "tourist;jiangly;Benq;Geothermal;ecnerwala;ksun48"
    how_many_contest_result = 10

    contest_list = fetch_contest_list(how_many_contest_result)
    user_infos = fetch_user_info(handles)
    contest_standing = fetch_contest_standings(contest_list, handles)
    response_user_list = build_leaderboard(user_infos, contest_list, contest_standing)

    cached_response = response_user_list
    return response_user_list

def fetch_contest_list(how_many_contest_result: int):
    """Fetch the list of recent contests."""
    api_url = "https://codeforces.com/api/contest.list?gym=false"
    response = requests.get(api_url)
    response.raise_for_status()

    contests = response.json().get('result', [])
    current_time = int(time.time())

    contest_list = [
        contest['id'] for contest in contests
        if contest.get('startTimeSeconds', 0) < current_time
    ]

    return contest_list[:how_many_contest_result]

def fetch_user_info(handles: str):
    """Fetch user information from Codeforces API."""
    fetch_user_info_url = f"https://codeforces.com/api/user.info?handles={handles}&checkHistoricHandles=false"
    response = requests.get(fetch_user_info_url)
    response.raise_for_status()

    return response.json().get('result', [])

def fetch_contest_standings(contest_list, handles: str):
    """Fetch contest standings for the given contests and users."""
    contest_standing = []

    for contest in contest_list:
        fetch_contest_info = f"https://codeforces.com/api/contest.standings?contestId={contest}&handles={handles}"
        response = requests.get(fetch_contest_info)
        response.raise_for_status()
        rows = response.json().get('result', {}).get('rows', [])

        for row in rows:
            contest_standing.append({
                'contestId': contest,
                'handle': row['party']['members'][0]['handle'],
                'rank': row['rank']
            })

    return contest_standing

def build_leaderboard(user_infos, contest_list, contest_standing):
    """Build the final leaderboard response."""
    response_user_list = []

    for user_info in user_infos:
        contest_standing_for_user = []

        for contest in contest_list:
            rank = next(
                (standing['rank'] for standing in contest_standing
                 if standing['handle'] == user_info['handle'] and standing['contestId'] == contest), 
                -1
            )
            contest_standing_for_user.append(rank)

        response_user_list.append({
            'handle': user_info['handle'],
            'name': f"{user_info.get('firstName', '')} {user_info.get('lastName', '')}",
            'rating': user_info.get('rating', 0),
            'max_rating': user_info.get('maxRating', 0),
            'contribution': user_info.get('contribution', 0),
            'rank': user_info.get('rank', ''),
            'contest_rank': contest_standing_for_user
        })

    return response_user_list
