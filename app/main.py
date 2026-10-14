from fastapi import FastAPI

from app.api.v1.router import api_router

app = FastAPI(
    title="TaskFlow API",
    description="Task management API with clean architecture",
    version="3.0.0",
)

app.include_router(api_router)


@app.get("/", tags=["Health"])
def home():
    return {"message": "Welcome to TaskFlow API"}


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy"}