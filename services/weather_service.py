import requests
from dotenv import load_dotenv
import os
from fastapi import HTTPException

load_dotenv()
api_key = os.getenv("OPENWEATHER_API_KEY")

if not api_key:
    raise ValueError("OPENWEATHER_API_KEY is not set in the environment variables.")

COMMON_TIMEOUT = 5
DEFAULT_ERROR_MESSAGE = "Error fetching data."
WEATHER_ERROR_MAP = {
    401: ("Invalid API key.", 401),
    404: ("City not found.", 404),
}


def fetch_api_json(
    url: str, params: dict, error_map: dict[int, tuple[str, int]] | None = None
) -> dict:
    try:
        response = requests.get(url, params=params, timeout=COMMON_TIMEOUT)
    except requests.exceptions.Timeout:
        raise HTTPException(status_code=504, detail="Request timed out.")
    except requests.exceptions.ConnectionError:
        raise HTTPException(status_code=503, detail="Service unavailable.")
    except requests.RequestException:
        raise HTTPException(status_code=500, detail=DEFAULT_ERROR_MESSAGE)

    if response.status_code == 200:
        return response.json()

    if error_map and response.status_code in error_map:
        detail, status = error_map[response.status_code]
        raise HTTPException(status_code=status, detail=detail)

    raise HTTPException(status_code=500, detail=DEFAULT_ERROR_MESSAGE)


def get_current_weather(city: str, units: str = "metric") -> dict:
    params = {"q": city, "appid": api_key, "units": units, "lang": "it"}
    data = fetch_api_json(
        "https://api.openweathermap.org/data/2.5/weather",
        params=params,
        error_map=WEATHER_ERROR_MAP,
    )

    return {
        "temperature": data["main"]["temp"],
        "description": data["weather"][0]["description"],
        "humidity": data["main"]["humidity"],
        "wind_speed": data["wind"]["speed"],
    }


def get_weather_forecast(city: str, units: str = "metric") -> dict:
    params = {"q": city, "appid": api_key, "units": units, "lang": "it"}
    data = fetch_api_json(
        "https://api.openweathermap.org/data/2.5/forecast",
        params=params,
        error_map=WEATHER_ERROR_MAP,
    )

    forecasts = [
        {
            "datetime": item["dt_txt"],
            "temperature": item["main"]["temp"],
            "description": item["weather"][0]["description"],
        }
        for item in data["list"]
    ]
    return {"city": city, "forecasts": forecasts}
