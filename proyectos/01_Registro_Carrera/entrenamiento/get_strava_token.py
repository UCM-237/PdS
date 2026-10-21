import requests
import webbrowser

CLIENT_ID = "192086"
CLIENT_SECRET = "e7ee4a247554a37d6cbbea26e98f162bbe966d79"
REDIRECT_URI = "http://localhost/exchange_token"
ACCESS_TOKEN = "93e0129fbbc699e1792898140ebafe8771173659"
REFRESH_TOKEN = "a0a8810e6708666365859e0acf600971a3986f85"

auth_url = (
    f"https://www.strava.com/oauth/authorize?"
    f"client_id={CLIENT_ID}&"
    f"response_type=code&"
    f"redirect_uri={REDIRECT_URI}&"
    f"approval_prompt=force&"
    f"scope=activity:read_all"
)

webbrowser.open(auth_url)
print("Autoriza la aplicación y copia el parámetro ?code=XXXX de la URL")