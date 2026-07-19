"""Entry point for the local AviOS web application."""

from pathlib import Path

from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from web.api_routes import router as api_router
from web.page_routes import router as page_router
from web.settings_routes import router as settings_router


BASE_DIR = Path(__file__).parent

app = FastAPI(title="AviOS Web API", version="0.3.0")
app.mount("/static", StaticFiles(directory=BASE_DIR / "web" / "static"), name="static")
app.include_router(api_router, prefix="/api")
app.include_router(page_router)
app.include_router(settings_router)
