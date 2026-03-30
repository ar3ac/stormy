from pydantic import BaseModel


class WeatherResponde(BaseModel):
    city: str
    temperature: float
    feels_like: float
    description: str
    humidity: int
    wind_speed: float
    icon: str
