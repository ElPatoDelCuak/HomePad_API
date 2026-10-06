from typing import List, Optional

from app.models.entities.inventory_entity import InventoryEntity
from app.models.repositories.inventory_repository import InventoryRepository
from app.schemas.inventory_schema import InventoryCreate, InventoryUpdate


class InventoryService:
    def __init__(self, repository: InventoryRepository):
        self.repository = repository

    def get_all(self) -> List[InventoryEntity]:
        return self.repository.get_all()

    def get_by_id(self, item_id: int) -> Optional[InventoryEntity]:
        return self.repository.get_by_id(item_id)

    def get_by_product_id(self, product_id: int) -> Optional[InventoryEntity]:
        return self.repository.get_by_product_id(product_id)

    def create(self, item_data: InventoryCreate) -> InventoryEntity:
        return self.repository.create(item_data)

    def update(self, item_id: int, item_data: InventoryUpdate) -> Optional[InventoryEntity]:
        return self.repository.update(item_id, item_data)

    def delete(self, item_id: int) -> bool:
        return self.repository.delete(item_id)