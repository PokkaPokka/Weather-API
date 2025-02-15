# Weather API

A FastAPI application that gathers current weather data for predefined cities and schedules regular updates using APScheduler.

## Setup Instructions

1. **Install dependencies**
   ```shell
   pip install -r requirements.txt
   ```
2. **Run the application**
   ```shell
   uvicorn app.main:app --reload
   ```

## Architecture Overview

1. **FastAPI**

   - Hosts the core API endpoints.
   - Uses `app/main.py` as the entry point.

2. **Routers**

   - Organizes related routes, such as the weather data routes inside `app/routers/weatherData.py`.

3. **Database**

   - Utilizes SQLAlchemy for ORM in `app.database.py`.
   - Stores weather data in the `WeatherData` model (defined in `app.models`).

4. **Scheduler**
   - Employs `apscheduler` for running daily tasks.
   - Starts in `main.py` and performs a daily (7 AM) weather update.

## Design Decisions Explanation

- **Layered Architecture**  
  Separates concerns across routers, models, and utilities to keep code maintainable.

- **Async I/O**  
  Utilizes `httpx.AsyncClient` for non-blocking requests, improving throughput for external API calls.

- **Environment Variables**  
  Uses `dotenv` to store API keys securely and keep secrets out of source code.
