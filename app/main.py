from fastapi import FastAPI
from .routers import weatherData

app = FastAPI()

app.include_router(weatherData.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
