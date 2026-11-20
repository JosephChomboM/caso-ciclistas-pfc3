from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text

from app.core.config import get_settings
from app.modules.cycleways.router import router as cycleways_router
from app.modules.parking.router import router as parking_router
from app.modules.users.router import router as users_router
from app.modules.users.service import Db

app = FastAPI(title="CicloLima", version="0.1.0")
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_settings().cors_origins,
    allow_methods=["GET", "POST", "PATCH", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)
app.include_router(users_router)
app.include_router(cycleways_router)
app.include_router(parking_router)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/ready")
def ready(db: Db):
    db.execute(text("SELECT 1"))
    return {"status": "ready"}


@app.middleware("http")
async def security_headers(request, call_next):
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
    response.headers["Cache-Control"] = "no-store"
    return response
