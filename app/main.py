from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.controllers import inventory_router, product_router, shopping_router


app = FastAPI(title="HomePad API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(product_router)
app.include_router(inventory_router)
app.include_router(shopping_router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok"}
