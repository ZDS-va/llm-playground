from fastapi import FastAPI
from app.api import v1
from fastapi.responses import HTMLResponse
from pathlib import Path

app = FastAPI()


app.include_router(v1.router,prefix="/api/v1")