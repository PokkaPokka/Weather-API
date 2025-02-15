from sqlalchemy import DateTime, Float, Column, Integer, String
from .database import Base


class WeatherData(Base):
    __tablename__ = "weather_data"

    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime(timezone=True), nullable=False)
    city = Column(String, nullable=False)
    temperature = Column(Float, nullable=False)
    feels_like = Column(Float, nullable=False)
    humidity = Column(Integer, nullable=False)
    pressure = Column(Integer, nullable=False)
    # weather data like rain, snow, etc.
    weather_condition = Column(String, nullable=False)
    # weather description like light rain, heavy snow, etc.
    condition_description = Column(String)
