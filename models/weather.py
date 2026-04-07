from pydantic import BaseModel


class WeatherResponse(BaseModel):
    city: str
    temperature: float
    # feels_like: float
    description: str
    humidity: int
    wind_speed: float
    # icon: str


class ForecastItem(BaseModel):
    datetime: str
    temperature: float
    description: str


class ForecastResponse(BaseModel):
    city: str
    forecasts: list[ForecastItem]
