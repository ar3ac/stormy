import requests
from dotenv import load_dotenv
import os
from fastapi import HTTPException

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

if not api_key:
    raise ValueError("OPENWEATHER_API_KEY is not set in the environment variables.")


def get_current_weather(city: str) -> dict:
    params = {"q": city, "appid": api_key, "units": "metric", "lang": "it"}
    response = requests.get(
        "https://api.openweathermap.org/data/2.5/weather", params=params
    )
    if response.status_code == 200:
        data = response.json()
        diz = {
            "temperature": data["main"]["temp"],
            "description": data["weather"][0]["description"],
            "humidity": data["main"]["humidity"],
            "wind_speed": data["wind"]["speed"],
        }
        return diz
    elif response.status_code == 404:
        raise HTTPException(status_code=404, detail="City not found.")
    elif response.status_code == 401:
        raise HTTPException(status_code=401, detail="Invalid API key.")
    else:
        raise HTTPException(status_code=500, detail="Error fetching weather data.")
