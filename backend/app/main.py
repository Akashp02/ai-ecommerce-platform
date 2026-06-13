from fastapi import FastAPI
from app.db.init_db import init_db
from app.api.user_routes import router as user_router
from app.api.auth_routes import router as auth_router
from app.core.config import settings
from app.api.product_routes import router as product_router

app = FastAPI(
    title=settings.app_name,
    version=settings.app_version
)
app.include_router(product_router)
app.include_router(user_router)
app.include_router(auth_router)

@app.get("/")
def root():
    return {
        "message": settings.app_name,
        "database": settings.database_url
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "environment": settings.environment
    }

@app.on_event("startup")
def startup():
    init_db()