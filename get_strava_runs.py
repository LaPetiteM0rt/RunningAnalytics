import requests

def get_strava_runs(access_token, activity_type="Run"):
    headers = {"Authorization": f"Bearer {access_token}"}
    all_runs = []
    page = 1

    while True:
        res = requests.get(
            "https://www.strava.com/api/v3/athlete/activities",
            headers=headers,
            params={"per_page": 200, "page": page}
        )
        data = res.json()

        if not data:
            break

        all_runs.extend(data)
        page += 1

    if activity_type:
        all_runs = [a for a in all_runs if a.get("sport_type") == activity_type]

    return all_runs