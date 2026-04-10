from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from dotenv import load_dotenv
import os
from routers.weather import router as weather_router

load_dotenv()
openweather_api_key = os.getenv("OPENWEATHER_API_KEY")
if not openweather_api_key:
    raise ValueError("OPENWEATHER_API_KEY is not set in the environment variables.")

app = FastAPI(
    title="stormy",
    description="Meteo in tempo reale per qualsiasi città",
    version="1.0.0",
)

app.include_router(weather_router)


@app.get("/", description="Root endpoint")
def read_root():
    return {"Hello": "World"}


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "status_code": 500},
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail, "status_code": exc.status_code},
    )
