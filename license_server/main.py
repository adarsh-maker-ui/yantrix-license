from fastapi import FastAPI

from license_server.database import engine
from license_server.models import Base
from license_server.routes.license import router as license_router


# -------------------------------------------------
# CREATE DATABASE TABLES ON STARTUP
# -------------------------------------------------
Base.metadata.create_all(bind=engine)


# -------------------------------------------------
# FASTAPI APP
# -------------------------------------------------
app = FastAPI(
    title="Yantrix License Server",
    description="Central license authority for Yantrix Core robots",
    version="1.0.0"
)


# -------------------------------------------------
# ROUTES
# -------------------------------------------------
app.include_router(license_router)


# -------------------------------------------------
# HEALTH / ROOT
# -------------------------------------------------
@app.get("/")
def root():
    return {
        "status": "ok",
        "service": "yantrix-license"
    }
