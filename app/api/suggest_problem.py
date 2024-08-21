import requests
from fastapi import APIRouter
router = APIRouter()


problems = []

def fetch_random_problem_not_solved(user_id):
    """Fetch a random problem that the user has not solved yet."""
    # Fetch user submissions
    fetch_user_info_url = f"https://codeforces.com/api/user.status?handle={user_id}"
    response = requests.get(fetch_user_info_url)
    response.raise_for_status()

    submissions = response.json().get('result', [])
    solved_problems = set()
    
    # Collect solved problems as tuples of (contestId, index)
    for submission in submissions:
        if submission['verdict'] == 'OK':
            solved_problems.add(
                (
                    submission['problem']['contestId'],
                    submission['problem']['index']
                )
            )

    # Fetch all problems
    if not problems:
        api_url = "https://codeforces.com/api/problemset.problems"
        response = requests.get(api_url)
        response.raise_for_status()

        problem_data = response.json().get('result', {})
        problems.extend(problem_data.get('problems', []))
    
    # Filter out solved problems
    unsolved_problems = [
        problem for problem in problems
        if (
            problem['contestId'],
            problem['index']
        ) not in solved_problems
    ]
    

    if not unsolved_problems:
        return None
    
    return unsolved_problems[0]


@router.get("/suggest-problem/{user_id}")   
def suggest_problem(user_id):
    """Fetches a random problem from Codeforces."""
    problem = fetch_random_problem_not_solved(user_id)
    return problem