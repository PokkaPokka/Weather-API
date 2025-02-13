import asyncio
import os
from dotenv import load_dotenv
from fastapi import Depends, HTTPException
import httpx
from sqlalchemy.orm import Session
from app import schemas
from app.models import WeatherData
from app.database import get_db
import datetime

load_dotenv()
api_key = os.getenv("API_KEY")


async def fetch_and_save_weather(
    weather: schemas.WeatherDataCreate,
    api_key: str,
    db: Session = Depends(get_db),
):
    # Get latitude and longitude for the city
    geocoding_url = "https://api.openweathermap.org/geo/1.0/direct"
    location = f"{weather.city}"
    geocoding_params = {"q": location, "appid": api_key, "limit": 1}

    async with httpx.AsyncClient() as client:
        # Fetch coordinates
        geocoding_response = await client.get(geocoding_url, params=geocoding_params)
        geocoding_response.raise_for_status()
        geocoding_data = geocoding_response.json()

        if not geocoding_data:
            raise HTTPException(
                status_code=404, detail=f"City {weather.city} not found"
            )

        lat = geocoding_data[0]["lat"]
        lon = geocoding_data[0]["lon"]

        # Fetch weather data using One Call API
        onecall_url = "https://api.openweathermap.org/data/3.0/onecall"
        onecall_params = {
            "lat": lat,
            "lon": lon,
            "appid": api_key,
            "units": "metric",
        }

        onecall_response = await client.get(onecall_url, params=onecall_params)
        onecall_response.raise_for_status()
        weather_data = onecall_response.json()

        # Extract relevant data
        current = weather_data["current"]
        weather_info = current["weather"][0]

        # Save to database
        db_weather = WeatherData(
            city=weather.city,
            temperature=current["temp"],
            feels_like=current["feels_like"],
            humidity=current["humidity"],
            pressure=current["pressure"],
            weather_condition=weather_info["main"],
            condition_description=weather_info["description"],
            created_at=datetime.datetime.now(),
        )
        db.add(db_weather)
        db.commit()
        db.refresh(db_weather)

        return db_weather
