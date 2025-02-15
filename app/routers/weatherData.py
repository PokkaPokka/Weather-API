import asyncio
import datetime
import logging
import os
from dotenv import load_dotenv
from fastapi import APIRouter, Depends, HTTPException, requests, status
from tenacity import *
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.utils import fetch_and_save_weather


router = APIRouter(prefix="/weatherData", tags=["weatherData"])
load_dotenv()
api_key = os.getenv("API_KEY")

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def is_retryable_exception(exception):
    return (
        isinstance(exception, HTTPException)
        and getattr(exception, "response", None)
        and exception.response.status_code != 404
    )


@router.post(
    "/getCityWeather",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.WeatherDataResponse,
)
@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=8),
    retry=retry_if_exception(is_retryable_exception),
)
async def get_weather(
    weather: schemas.WeatherDataCreate,
    db: Session = Depends(get_db),
):
    try:
        if not weather.city.strip():
            raise HTTPException(status_code=400, detail="City name is required")

        weather_record = await fetch_and_save_weather(weather, api_key, db)

        # Clear any weather data older than 3 days.
        three_days_ago = weather_record.created_at - datetime.timedelta(days=3)
        db.query(models.WeatherData).filter(
            models.WeatherData.created_at < three_days_ago
        ).delete(synchronize_session=False)
        db.commit()
        return weather_record
    except HTTPException as http_exc:
        logger.error(f"HTTP error occurred: {http_exc.detail}")
        raise http_exc
    except Exception as e:
        logger.error(f"An error occurred: {str(e)}")
        raise HTTPException(status_code=500, detail="Internal Server Error")


def call_get_weather(weather_data: schemas.WeatherDataCreate):
    try:
        db: Session = next(get_db())
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(get_weather(weather_data, db))
        loop.close()
    except Exception as e:
        print(f"Error calling weather function: {e}")
