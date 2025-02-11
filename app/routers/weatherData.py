from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.models import WeatherData
from app.database import get_db

router = APIRouter(prefix="/weatherData", tags=["weatherData"])


@router.get("/")
def read_weather(db: Session = Depends(get_db)):
    weather_data = db.query(WeatherData).all()
    return weather_data
