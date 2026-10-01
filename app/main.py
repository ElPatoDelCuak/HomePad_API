from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.config import settings
from app.database import Base, engine
from app.controllers import inventory_controller, product_controller, shopping_controller


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Ensure database tables exist on startup
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(
    title="HomePad API",
    description="REST API for managing home inventory and shopping list",
    version="1.0.0",
    lifespan=lifespan,
    debug=settings.DEBUG,
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API Routers under /api/v1
app.include_router(product_controller.router, prefix="/api/v1")
app.include_router(inventory_controller.router, prefix="/api/v1")
app.include_router(shopping_controller.router, prefix="/api/v1")


@app.get("/", tags=["Health"])
def health_check():
    return {
        "status": "online",
        "app": "HomePad API",
        "version": "1.0.0",
        "env": settings.APP_ENV
    }
