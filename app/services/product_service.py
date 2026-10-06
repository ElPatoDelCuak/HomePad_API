from typing import List, Optional

from app.models.entities.product_entity import ProductEntity
from app.models.repositories.product_repository import ProductRepository
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    def get_all(self) -> List[ProductEntity]:
        return self.repository.get_all()

    def get_by_id(self, product_id: int) -> Optional[ProductEntity]:
        return self.repository.get_by_id(product_id)

    def get_by_name(self, name: str) -> Optional[ProductEntity]:
        return self.repository.get_by_name(name)

    def create(self, product_data: ProductCreate) -> ProductEntity:
        return self.repository.create(product_data)

    def update(self, product_id: int, product_data: ProductUpdate) -> Optional[ProductEntity]:
        return self.repository.update(product_id, product_data)

    def delete(self, product_id: int) -> bool:
        return self.repository.delete(product_id)