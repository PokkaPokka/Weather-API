# Weather API

A simple FastAPI application that gathers current weather data for predefined cities and schedules regular updates using APScheduler.

## Setup and Installation

1. **Install dependencies**
   ```shell
   pip install -r requirements.txt
   ```
2. **Run the application**
   ```shell
   uvicorn app.main:app --reload
   ```

## Project Structure

- **app/main.py**  
  Initializes the FastAPI application, sets up a scheduler to fetch weather data daily at 7am for a list of cities, and shuts down the scheduler when the app stops.
- **app/routers/weatherData.py**  
  Contains the routes for weather-related operations.
- **app/schemas.py**  
  Defines data models per FastAPI’s pydantic structures.

## Scheduler Details

- Uses a `BackgroundScheduler` with a cron trigger set for 7:00 AM.
- Fetches weather data for each city in the `cities` list.
- Shuts down gracefully using an `asynccontextmanager`.
