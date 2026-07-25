import webbrowser
import requests
import json
import subprocess
import os
import winreg
from http.server import BaseHTTPRequestHandler, HTTPServer
from dotenv import load_dotenv

load_dotenv()
CLIENT_ID = os.environ["STRAVA_CLIENT_ID"]
CLIENT_SECRET = os.environ["STRAVA_CLIENT_SECRET"]

REDIRECT_URI = "http://127.0.0.1:8080"
TOKEN_FILE = "tokens.json"

def open_browser(url):
    try:
        with (winreg.OpenKey(winreg.HKEY_CURRENT_USER,
                           r"Software\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice")
              as key):
            prog_id = winreg.QueryValueEx(key, "ProgId")[0]

        with winreg.OpenKey(winreg.HKEY_CLASSES_ROOT,
                           rf"{prog_id}\shell\open\command") as key:
            cmd = winreg.QueryValueEx(key, "")[0]

        exe = cmd.split('"')[1] if '"' in cmd else cmd.split()[0]
        subprocess.Popen([exe, url])

    except Exception:
        webbrowser.open(url)

# TOKEN STORAGE
def load_tokens():
    try:
        if not os.path.exists(TOKEN_FILE):
            return None

        with open(TOKEN_FILE, "r") as f:
            data = f.read().strip()
            if not data:
                return None
            return json.loads(data)

    except:
        return None


def save_tokens(tokens):
    with open(TOKEN_FILE, "w") as f:
        json.dump(tokens, f)

# OAUTH FLOW
def get_authorization_code():
    auth_url = (
        f"https://www.strava.com/oauth/authorize"
        f"?client_id={CLIENT_ID}"
        f"&response_type=code"
        f"&redirect_uri={REDIRECT_URI}"
        f"&approval_prompt=force"
        f"&scope=read,activity:read_all"
    )

    print("\nOPENING STRAVA LOGIN...\n")

    open_browser(auth_url)

    print("Waiting for authorization callback...")

    code_holder = {}

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if "code=" in self.path:
                code_holder["code"] = self.path.split("code=")[1].split("&")[0]

            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"You can close this window.")

        def log_message(self, fmt, *args):
            return

    server = HTTPServer(("127.0.0.1", 8080), Handler)
    server.handle_request()

    return code_holder["code"]

# EXCHANGE CODE -> TOKEN
def exchange_code(code):
    res = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "code": code,
            "grant_type": "authorization_code"
        }
    )
    return res.json()

# REFRESH TOKEN
def refresh_token(token_value):
    res = requests.post(
        "https://www.strava.com/oauth/token",
        data={
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
            "grant_type": "refresh_token",
            "refresh_token": token_value
        }
    )
    return res.json()

# GET ACTIVITIES
def get_all_activities(access_token, activity_type="Run"):
    headers = {"Authorization": f"Bearer {access_token}"}
    all_activities = []
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

        all_activities.extend(data)
        page += 1

    if activity_type:
        all_activities = [a for a in all_activities if a.get("sport_type") == activity_type]

    return all_activities

# MAIN
def main():
    tokens = load_tokens()

    # FIRST RUN
    if not tokens:
        print("No tokens → OAuth flow")

        code = get_authorization_code()
        tokens = exchange_code(code)

        save_tokens(tokens)

    # NEXT RUNS
    else:
        print("Refreshing token...")

        tokens = refresh_token(tokens["refresh_token"])
        save_tokens(tokens)

    if not tokens or "access_token" not in tokens:
        print("Token error:", tokens)
        return

    access_token = tokens["access_token"]

    activities = get_all_activities(access_token)
    os.makedirs("data/raw", exist_ok=True)

    with open("data/raw/activities.json", "w") as f:
        json.dump(activities, f, indent=2)

if __name__ == "__main__":
    main()