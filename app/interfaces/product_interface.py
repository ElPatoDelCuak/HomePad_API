from typing import Protocol
from app.models.entities.product_entity import ProductEntity
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductRepositoryProtocol(Protocol):
    def get_all(self) -> list[ProductEntity]:
        ...

    def get_by_id(self, product_id: int) -> ProductEntity | None:
        ...

    def get_by_name(self, name: str) -> ProductEntity | None:
        ...

    def create(self, product_data: ProductCreate) -> ProductEntity:
        ...

    def update(self, product_id: int, product_data: ProductUpdate) -> ProductEntity | None:
        ...

    def delete(self, product_id: int) -> bool:
        ...
