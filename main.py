from fastapi import FastAPI
from dotenv import load_dotenv
import os

load_dotenv()
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
if not openweather_api_key:
    raise ValueError("OPENWEATHER_API_KEY is not set in the environment variables.")

app = FastAPI(
    title="stormy",
    description="Meteo in tempo reale per qualsiasi città",
    version="1.0.0",
)


@app.get("/", description="Root endpoint")
def read_root():
    return {"Hello": "World"}
