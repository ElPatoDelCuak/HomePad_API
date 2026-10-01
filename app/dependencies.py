from collections.abc import Generator
from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.interfaces.inventory_interface import InventoryRepositoryProtocol
from app.interfaces.product_interface import ProductRepositoryProtocol
from app.interfaces.shopping_interface import ShoppingRepositoryProtocol
from app.models.repositories.inventory_repository import InventoryRepository
from app.models.repositories.product_repository import ProductRepository
from app.models.repositories.shopping_repository import ShoppingRepository
from app.services.inventory_service import InventoryService
from app.services.product_service import ProductService
from app.services.shopping_service import ShoppingService


def get_product_repository(db: Session = Depends(get_db)) -> ProductRepositoryProtocol:
    return ProductRepository(db)


def get_inventory_repository(db: Session = Depends(get_db)) -> InventoryRepositoryProtocol:
    return InventoryRepository(db)


def get_shopping_repository(db: Session = Depends(get_db)) -> ShoppingRepositoryProtocol:
    return ShoppingRepository(db)


def get_product_service(
    product_repo: ProductRepositoryProtocol = Depends(get_product_repository),
) -> ProductService:
    return ProductService(product_repo=product_repo)


def get_inventory_service(
    inventory_repo: InventoryRepositoryProtocol = Depends(get_inventory_repository),
    product_repo: ProductRepositoryProtocol = Depends(get_product_repository),
) -> InventoryService:
    return InventoryService(
        inventory_repo=inventory_repo,
        product_repo=product_repo,
    )


def get_shopping_service(
    shopping_repo: ShoppingRepositoryProtocol = Depends(get_shopping_repository),
    inventory_repo: InventoryRepositoryProtocol = Depends(get_inventory_repository),
    product_repo: ProductRepositoryProtocol = Depends(get_product_repository),
) -> ShoppingService:
    return ShoppingService(
        shopping_repo=shopping_repo,
        inventory_repo=inventory_repo,
        product_repo=product_repo,
    )
