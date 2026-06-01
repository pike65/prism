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

app.mount(
    "/styles", 
    StaticFiles(directory=Path(__file__).parent.parent.parent / "frontend" / "src" / "styles"), 
    name="styles"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(media_router)


@app.get("/", response_class=HTMLResponse)
def get_dashboard():
    html_path = Path(__file__).parent.parent.parent / "frontend" / "src" / "dashboard.html"
    
    with open(html_path, "r", encoding="utf-8") as file:
        return file.read()
