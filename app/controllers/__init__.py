from app.controllers.inventory_controller import router as inventory_router
from app.controllers.product_controller import router as product_router
from app.controllers.shopping_controller import router as shopping_router

__all__ = ["inventory_router", "product_router", "shopping_router"]