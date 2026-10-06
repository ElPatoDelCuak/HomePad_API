from typing import Protocol, List, Optional
from app.schemas.inventory_schema import InventoryCreate, InventoryUpdate
from app.models.entities.inventory_entity import InventoryEntity

class IInventoryRepository(Protocol):
    def get_all(self) -> List[InventoryEntity]:
        ...

    def get_by_id(self, item_id: int) -> Optional[InventoryEntity]:
        ...

    def get_by_product_id(self, product_id: int) -> Optional[InventoryEntity]:
        ...

    def create(self, item_data: InventoryCreate) -> InventoryEntity:
        ...

    def update(self, item_id: int, item_data: InventoryUpdate) -> Optional[InventoryEntity]:
        ...

    def delete(self, item_id: int) -> bool:
        ...