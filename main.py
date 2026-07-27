import os
import json
import strava_auth
import get_strava_runs
from data_processor import process_raw_data


def main():
    tokens = strava_auth.load_tokens()

    # FIRST RUN
    if not tokens:
        print("No tokens → OAuth flow")

        code = strava_auth.get_authorization_code()
        tokens = strava_auth.exchange_code(code)

        strava_auth.save_tokens(tokens)

    # NEXT RUNS
    else:
        print("Refreshing token...")

        tokens = strava_auth.refresh_token(tokens["refresh_token"])
        strava_auth.save_tokens(tokens)

    if not tokens or "access_token" not in tokens:
        print("Token error:", tokens)
        return

    access_token = tokens["access_token"]

    activities = get_strava_runs.get_strava_runs(access_token)
    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/runs_raw.json", "w") as f:
        json.dump(activities, f, indent=2)

process_raw_data("data/raw/runs_raw.json")

if __name__ == "__main__":
    main()