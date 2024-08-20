from fastapi import APIRouter
import requests
import time

router = APIRouter()

cached_response = False

@router.get("/")
def read_root():
    return {"message": "Hello, World!"}

@router.get("/leaderboard")
def get_leaderboard():
    global cached_response
    if cached_response:
        return cached_response

    # Predefined list of user handles (this will later be fetched from the database)
    handles = "tourist;jiangly;Benq;Geothermal;ecnerwala;ksun48"

    # Number of contest results to fetch for each user
    how_many_contest_result = 10

    # Fetch the contest list
    api_url = "https://codeforces.com/api/contest.list?gym=false"
    response = requests.get(api_url)
    response.raise_for_status()

    contests = response.json().get('result', [])
    
    current_time = int(time.time())  # Get the current system time in seconds

    contest_list = []
    for contest in contests:
        start_time_seconds = contest.get('startTimeSeconds', 0)
        if start_time_seconds < current_time:
            contest_list.append(contest['id'])
            
    contest_list = contest_list[:how_many_contest_result]

    # Fetch user information from Codeforces API
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

        for row in rows:
            contest_standing.append({
                'contestId': contest,
                'handle': row['party']['members'][0]['handle'],
                'rank': row['rank']
            })
    
    # Prepare the final leaderboard response
    response_user_list = []
    for user_info in user_infos:
        contest_standing_for_user = []
        for contest in contest_list:
            flag = 0
            for standing in contest_standing:
                if standing['handle'] == user_info['handle'] and standing['contestId'] == contest:
                    contest_standing_for_user.append(standing['rank'])
                    flag = 1
                    break
            if flag == 0:
                contest_standing_for_user.append(-1)
        response_user_list.append({
            'handle': user_info['handle'],
            'name': user_info.get('firstName', '') + " " + user_info.get('lastName', ''),
            'rating': user_info.get('rating', 0),
            'max_rating': user_info.get('maxRating', 0),
            'contribution': user_info.get('contribution', 0),
            'rank': user_info.get('rank', ''),
            'contest_rank': contest_standing_for_user
        })
    
    cached_response = response_user_list
    return response_user_list

