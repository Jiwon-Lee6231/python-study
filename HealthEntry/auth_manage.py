import json
import requests

from urllib.parse import urlparse, parse_qsl
from google_auth_oauthlib.flow import InstalledAppFlow

CLIENT_SECRETS_FILE = 'all_auth/client_secret.json'

SCOPES = [
    'https://www.googleapis.com/auth/youtube',
    'https://www.googleapis.com/auth/youtube.force-ssl',
    'https://www.googleapis.com/auth/youtube.readonly',
    'https://www.googleapis.com/auth/youtubepartner',
    'https://www.googleapis.com/auth/calendar',
    'https://www.googleapis.com/auth/calendar.events',
    'https://www.googleapis.com/auth/calendar.events.readonly',
    'https://www.googleapis.com/auth/calendar.readonly'
]

def get_authenticated_google():
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRETS_FILE, SCOPES)
    credentials = flow.run_console()

    return credentials

def save_api_info(url_type, client_id, client_secret="null", state="null"):
    auth_data = {
        "client_id": client_id
    }

    # 네이버인 경우 client_secret이 있음
    if url_type == "naver":
        auth_data['client_secret'] = client_secret
        auth_data['state'] = state

    with open("all_auth/" + url_type + "_auth.json", "w") as fp:
        json.dump(auth_data, fp)

# https://kauth.kakao.com/oauth/authorize?client_id={API_KEY}&redirect_uri=https://localhost.com&response_type=code&scope=talk_message
# 로그인
def login_auth(url_type):
    with open("all_auth/" + url_type + "_auth.json", "r") as fp:
        auth_data = json.load(fp)

    data = "response_type=code&" + \
           "client_id=" + auth_data['client_id'] + "&" + \
           "redirect_uri=https://localhost.com"

    if url_type == "kakao":
        url = "https://kauth.kakao.com/oauth/authorize?"

        data += "&scope=talk_message"

    elif url_type == "naver":
        url = "https://nid.naver.com/oauth2.0/authorize?"

        data += "&state=" + auth_data['state']

    response = requests.get(url + data)

    return response.url


# 로그인 후, url 그대로 입력하면 code값만 추출
def save_code(url_type, url):
    with open("all_auth/" + url_type + "_auth.json", "r") as fp:
        auth_data = json.load(fp)

    url = urlparse(url)
    url_args = dict(parse_qsl(url.query))

    auth_data['code'] = url_args['code']

    with open("all_auth/" + url_type + "_auth.json", "w") as fp:
        json.dump(auth_data, fp)

# 토큰 발급
def create_token(url_type):
    with open("all_auth/" + url_type + "_auth.json", "r") as fp:
        auth_data = json.load(fp)

    data = {
        "grant_type": "authorization_code",
        "client_id": auth_data['client_id'],
        "code": auth_data['code']
    }

    if url_type == "kakao":
        url = "https://kauth.kakao.com/oauth/token"

        data['redirect_uri'] = "https://localhost.com"

    elif url_type == "naver":
        url = "https://nid.naver.com/oauth2.0/token"

        data['client_secret'] = auth_data['client_secret']
        data['state'] = auth_data['state']

    response = requests.post(url, data=data)
    tokens = response.json()

    with open("all_auth/" + url_type + "_code.json", "w") as fp:
        json.dump(tokens, fp)

    return tokens


# 로그인 KEY, SECRET 불러오기
def get_auth(url_type):
    with open("all_auth/" + url_type + "_auth.json", "r") as fp:
        auth_data = json.load(fp)

    auths = {
        "client_id": auth_data['client_id']
    }

    if url_type == "naver":
        auths['client_secret'] = auth_data['client_secret']

    return auths


# 토큰 불러오기
def get_token(url_type, is_refresh=False):
    file_name = "all_auth/" + url_type + "_code.json"

    if is_refresh:
        file_name = "all_auth/" + url_type + "_code_refresh.json"

    with open(file_name, "r") as fp:
        code_data = json.load(fp)

    headers = {
        "Authorization": "Bearer " + code_data['access_token']
    }

    return headers


# 토큰 갱신
def refresh_token(url_type):
    with open("all_auth/" + url_type + "_auth.json", "r") as fp:
        auth_data = json.load(fp)

    with open("all_auth/" + url_type + "_code.json", "r") as fp:
        code_data = json.load(fp)

    data = {
        "grant_type": "refresh_token",
        "client_id": auth_data['client_id'],
        "refresh_token": code_data['refresh_token']
    }

    if url_type == "kakao":
        url = "https://kauth.kakao.com/oauth/token"

    elif url_type == "naver":
        url = "https://nid.naver.com/oauth2.0/token"

        data['client_secret'] = auth_data['client_secret']

    response = requests.post(url, data=data)
    refresh_tokens = response.json()

    with open("all_auth/" + url_type + "_code_refresh.json", "w") as fp:
        json.dump(refresh_tokens, fp)

    return refresh_tokens


if __name__ == "__main__":
    # print(login_auth("kakao"))
    save_code("kakao", "https://localhost.com/?code=ITV9YFc9umr4MMOYYeWMACNDqvDg3qVZkUS0BTHtRCK4i9mbCBCUkgDUdiEQMXs8IzH1ZworDKYAAAFy9IUPYg")
    create_token("kakao")
    # get_token("kakao")



