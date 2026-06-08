from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from database.session import engine, Base
from database.models import media as media_models
from api.media import router as media_router


Base.metadata.create_all(bind=engine)

app = FastAPI(title="Prism")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(media_router)


@app.get("/")
def root():
    return {"system": "on"}
