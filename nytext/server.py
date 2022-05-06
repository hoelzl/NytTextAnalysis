import json
from pathlib import Path
from fastapi import FastAPI, Response
from modulefinder import ModuleFinder
from .config import get_archive_file_path

app = FastAPI()


@app.get("/")
async def status_message():
    return {"status": "running"}


@app.get("/news/{year}/{month}")
async def news(year: int, month: int, response: Response):
    path = get_archive_file_path(year, month)
    try:
        with open(path, "r", encoding="utf-8") as file:
            payload = json.load(file)
        return payload
    except FileNotFoundError:
        # Use the status code the NYT returns when accessing a date for which no data is
        # available.
        response.status_code = 403
        return {}
