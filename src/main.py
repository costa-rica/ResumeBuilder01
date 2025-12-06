from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from src.routes import builder
import os

app = FastAPI(title="ResumeBuilder01")

# Mount static files
static_path = os.path.join(os.path.dirname(__file__), "static")
if not os.path.exists(static_path):
    os.makedirs(static_path)
app.mount("/static", StaticFiles(directory=static_path), name="static")

# Include routers
app.include_router(builder.router)

@app.get("/health")
async def health_check():
    return {"status": "ok"}
