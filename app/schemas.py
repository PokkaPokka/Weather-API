from datetime import datetime
from pydantic import BaseModel


class WeatherDataBase(BaseModel):
    city: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    weather_condition: str
    condition_description: str


class WeatherDataCreate(BaseModel):
    city: str


class WeatherDataResponse(BaseModel):
    id: int
    city: str
    temperature: float
    feels_like: float
    humidity: int
    pressure: int
    weather_condition: str
    condition_description: str
    created_at: datetime

    class Config:
        orm_mode = True
