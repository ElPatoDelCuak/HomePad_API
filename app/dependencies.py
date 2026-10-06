from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.repositories.inventory_repository import InventoryRepository
from app.models.repositories.product_repository import ProductRepository
from app.models.repositories.shopping_repository import ShoppingRepository
from app.services.inventory_service import InventoryService
from app.services.product_service import ProductService
from app.services.shopping_service import ShoppingService


def get_inventory_service(db: Session = Depends(get_db)) -> InventoryService:
    return InventoryService(InventoryRepository(db))


def get_product_service(db: Session = Depends(get_db)) -> ProductService:
    return ProductService(ProductRepository(db))


def get_shopping_service(db: Session = Depends(get_db)) -> ShoppingService:
    return ShoppingService(ShoppingRepository(db))