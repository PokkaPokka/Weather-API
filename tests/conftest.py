from fastapi.testclient import TestClient
from app.main import app
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.database import get_db, Base
import os
import pytest


URL = f'postgresql://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@{os.getenv("DB_HOST")}/{os.getenv("DB_NAME")}_test'
if URL is None:
    raise ValueError("No DATABASE_URL found in environment variables")

engine = create_engine(URL)
TestSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


client = TestClient(app)


# Drop all tables and recreate them before tests
@pytest.fixture
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Override the get_db dependency to use the TestSessionLocal
@pytest.fixture
def client(session):
    def override_get_db():
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = override_get_db
    yield TestClient(app)


# Create a test weather data
@pytest.fixture
def test_weather(client):
    weather_city = {"city": "London"}
    response = client.post("/weatherData/getCityWeather/", json=weather_city)
    new_weather = response.json()
    assert response.status_code == 201
    return new_weather
