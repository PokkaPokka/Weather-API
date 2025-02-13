from contextlib import asynccontextmanager
from fastapi import FastAPI

from app import schemas
from .routers import weatherData
from apscheduler.schedulers.background import (
    BackgroundScheduler,
)  # runs tasks in the background
from apscheduler.triggers.cron import (
    CronTrigger,
)  # allows us to specify a recurring time for execution

app = FastAPI()

app.include_router(weatherData.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


cities = ["London", "Boston", "Tokyo"]
scheduler = BackgroundScheduler()
morningTrigger = CronTrigger(hour=7, minute=0)
for city in cities:
    weather_data = schemas.WeatherDataCreate(city=city)
    scheduler.add_job(
        weatherData.call_get_weather, trigger=morningTrigger, args=[weather_data]
    )
scheduler.start()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    scheduler.shutdown()
