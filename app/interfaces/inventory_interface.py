from decimal import Decimal
from typing import Protocol
from app.models.entities.inventory_entity import InventoryEntity
from app.schemas.inventory_schema import InventoryCreate, InventoryUpdate


class InventoryRepositoryProtocol(Protocol):
    def get_all(self) -> list[InventoryEntity]:
        ...

    def get_by_id(self, item_id: int) -> InventoryEntity | None:
        ...

    def get_by_product_id(self, product_id: int) -> InventoryEntity | None:
        ...

    def create(self, inventory_data: InventoryCreate) -> InventoryEntity:
        ...

    def update(self, item_id: int, inventory_data: InventoryUpdate) -> InventoryEntity | None:
        ...

    def add_quantity(self, product_id: int, quantity: Decimal) -> InventoryEntity:
        ...

    def delete(self, item_id: int) -> bool:
        ...
