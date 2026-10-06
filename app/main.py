from fastapi import FastAPI

from app.controllers import inventory_router, product_router, shopping_router


app = FastAPI(title="HomePad API")

app.include_router(product_router)
app.include_router(inventory_router)
app.include_router(shopping_router)


@app.get("/", tags=["health"])
def health_check():
    return {"status": "ok"}