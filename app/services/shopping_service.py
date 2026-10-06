from typing import List, Optional

from app.models.entities.shopping_entity import ShoppingEntity
from app.models.repositories.shopping_repository import ShoppingRepository
from app.schemas.shopping_schema import ShoppingCreate, ShoppingUpdate


class ShoppingService:
    def __init__(self, repository: ShoppingRepository):
        self.repository = repository

    def get_all(self) -> List[ShoppingEntity]:
        return self.repository.get_all()

    def get_by_id(self, item_id: int) -> Optional[ShoppingEntity]:
        return self.repository.get_by_id(item_id)

    def get_picked_items(self) -> List[ShoppingEntity]:
        return self.repository.get_picked_items()

    def create(self, item_data: ShoppingCreate) -> ShoppingEntity:
        return self.repository.create(item_data)

    def update(self, item_id: int, item_data: ShoppingUpdate) -> Optional[ShoppingEntity]:
        return self.repository.update(item_id, item_data)

    def delete(self, item_id: int) -> bool:
        return self.repository.delete(item_id)

    def delete_many(self, item_ids: List[int]) -> bool:
        return self.repository.delete_many(item_ids)