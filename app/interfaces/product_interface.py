from typing import Protocol, List, Optional
from app.schemas.product_schema import ProductCreate, ProductUpdate
from app.models.entities.product_entity import ProductEntity

class IProductRepository(Protocol):
    def get_all(self) -> List[ProductEntity]:
        ...

    def get_by_id(self, product_id: int) -> Optional[ProductEntity]:
        ...

    def get_by_name(self, name: str) -> Optional[ProductEntity]:
        ...

    def create(self, product_data: ProductCreate) -> ProductEntity:
        ...

    def update(self, product_id: int, product_data: ProductUpdate) -> Optional[ProductEntity]:
        ...

    def delete(self, product_id: int) -> bool:
        ...