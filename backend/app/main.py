from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from uuid import UUID
from sqlalchemy.orm import Session

from schemas.media import *


app = FastAPI(title="Prism", description="Content Tracker", version="0.1.0")


media_db = []


@app.get("/")
def root():
    return FileResponse("app/static/dashboard.html")


@app.post("/media")
def create_media(media_input: MediaInput):
    media_db.append(media_input)
    return media_input


@app.get("/media")
def get_all_media():
    return media_db
