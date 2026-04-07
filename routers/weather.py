from fastapi import APIRouter
from services.weather_service import get_current_weather, get_weather_forecast
from models.weather import ForecastResponse, ForecastItem
from models.weather import WeatherResponse

# Crei la mini-app (router) specifica per il meteo
router = APIRouter(
    prefix="/weather",
    tags=["weather"],
)


# aggiungere query parameter per unità di misura (metric, imperial, standard)
@router.get(
    "/{city}",
    description="Get current weather for a city",
    response_model=WeatherResponse,
)
def get_weather(city: str, units: str = "metric"):
    weather_data = get_current_weather(city, units)
    return WeatherResponde(
        city=city,
        temperature=weather_data["temperature"],
        description=weather_data["description"],
        humidity=weather_data["humidity"],
        wind_speed=weather_data["wind_speed"],
    )


@router.get(
    "/{city}/forecast",
    description="Get weather forecast for a city",
    response_model=ForecastResponse,
)
def get_forecast(city: str):
    forecast_data = get_weather_forecast(city)
    return ForecastResponse(
        city=forecast_data["city"],
        forecasts=[ForecastItem(**item) for item in forecast_data["forecasts"]],
    )
