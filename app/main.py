from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.v1.router import api_router
from app.core.config import settings


app = FastAPI(
    title="TaskFlow API",
    description="Task management API with clean architecture",
    version="3.0.0",
)

# Dynamically inject CORS configuration if origins are present
if settings.CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        # Strip trailing slashes safely to prevent strict string mismatch errors
        allow_origins=[origin.rstrip("/") for origin in settings.CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_router)


@app.get("/", tags=["Health"])
def home():
    return {"message": "Welcome to TaskFlow API"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}