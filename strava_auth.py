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