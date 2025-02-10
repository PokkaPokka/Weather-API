import os
import requests
from dotenv import load_dotenv
from fastapi import FastAPI

app = FastAPI()
load_dotenv()
api_key = os.getenv("API_KEY")


@app.get("/")
async def root():
    return {"message": "Hello World"}
