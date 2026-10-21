import os
import webbrowser

# El identificador de la aplicación de Strava se lee de una variable de entorno:
#   export STRAVA_CLIENT_ID=...
CLIENT_ID = os.environ["STRAVA_CLIENT_ID"]
REDIRECT_URI = "http://localhost/exchange_token"

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