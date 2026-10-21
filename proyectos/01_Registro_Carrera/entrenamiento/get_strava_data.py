import requests
import pandas as pd
import matplotlib.pyplot as plt

REFRESH_TOKEN = "03dc894b2a65a2b39ffad8659a6a0a8490349e05"
ACCESS_TOKEN = "fbb21c238a1327f7dfaef7003350470eb999cb06"

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
