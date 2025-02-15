import pytest


def test_create_weather_existing_city(client):
    # Test how the endpoint handles a city that already exists
    weather_city = {"city": "New York"}
    response = client.post("/weatherData/getCityWeather/", json=weather_city)
    assert response.status_code in [200, 201]  # Depending on API logic
    data = response.json()
    assert data["city"] == "New York"


def test_create_weather_empty_city(client):
    # Test an empty city payload
    weather_city = {"city": ""}
    response = client.post("/weatherData/getCityWeather/", json=weather_city)
    assert response.status_code == 400


def test_create_weather_numeric_city(client):
    # Test a numeric city name
    weather_city = {"city": "12345"}
    response = client.post("/weatherData/getCityWeather/", json=weather_city)
    assert response.status_code in [200, 404]  # Depending on API logic


def test_create_weather_special_characters_city(client):
    # Test a city name with special characters
    weather_city = {"city": "@#$%^&*"}
    response = client.post("/weatherData/getCityWeather/", json=weather_city)
    assert response.status_code in [400, 404]
