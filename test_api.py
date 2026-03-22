import requests
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("API_KEY")


params = {"q": "Lecco", "appid": API_KEY, "units": "metric", "lang": "it"}

response = requests.get(
    "https://api.openweathermap.org/data/2.5/weather", params=params
)
if response.status_code == 200:
    # print(response.json())
    print("Temperature:", response.json()["main"]["temp"], "°C")
    print("Description:", response.json()["weather"][0]["description"])
    print("Humidity:", response.json()["main"]["humidity"], "%")
    print("Wind speed:", response.json()["wind"]["speed"], "m/s")
else:
    print("Error:", response.status_code)
