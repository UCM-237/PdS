import os

import requests
import pandas as pd

# El token de acceso se lee de una variable de entorno para no guardarlo en el repositorio:
#   export STRAVA_ACCESS_TOKEN=...
ACCESS_TOKEN = os.environ["STRAVA_ACCESS_TOKEN"]

def get_activities():
  headers = {
      "Authorization": f"Bearer {ACCESS_TOKEN}"
  }
  url = "https://www.strava.com/api/v3/athlete/activities"
  params = {"per_page": 5, "page": 1}

  return requests.get(url, headers=headers, params=params).json()


def get_activity(activity_id, stream_types="time,distance,heartrate,velocity_smooth,altitude"):
  url = f"https://www.strava.com/api/v3/activities/{activity_id}/streams"
  headers = {
      "Authorization": f"Bearer {ACCESS_TOKEN}"
  }
  params = {
    "keys": stream_types,
    "key_by_type": "true"
  }
  streams = requests.get(url, headers=headers, params=params).json()
  data = {
      "time": streams["time"]["data"],
      "distance": streams["distance"]["data"],
      "heartrate": streams.get("heartrate", {}).get("data", []),
      "velocity": streams.get("velocity_smooth", {}).get("data", []),
      "altitude": streams.get("altitude", {}).get("data", [])
  }
  df = pd.DataFrame(data)
  df["distance_km"] = df["distance"] / 1000
  df["speed_kmh"] = df["velocity"] * 3.6
  return df

activities = get_activities()

for a in activities:
  data = get_activity(a['id'])
  print(f'Descargada actividad "{a["name"]}" en archivo "data_{a["start_date"]}.csv"')
  data.to_csv(f'data_{a["start_date"]}.csv')
