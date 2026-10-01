from typing import Protocol
from app.models.entities.shopping_entity import ShoppingItemEntity
from app.schemas.shopping_schema import ShoppingItemCreate, ShoppingItemUpdate


class ShoppingRepositoryProtocol(Protocol):
    def get_all(self) -> list[ShoppingItemEntity]:
        ...

    def get_by_id(self, item_id: int) -> ShoppingItemEntity | None:
        ...

    def get_by_product_id(self, product_id: int) -> ShoppingItemEntity | None:
        ...

    def get_picked_items(self) -> list[ShoppingItemEntity]:
        ...

    def create(self, shopping_data: ShoppingItemCreate) -> ShoppingItemEntity:
        ...

    def update(self, item_id: int, shopping_data: ShoppingItemUpdate) -> ShoppingItemEntity | None:
        ...

    def delete(self, item_id: int) -> bool:
        ...

    def delete_items(self, item_ids: list[int]) -> None:
        ...
