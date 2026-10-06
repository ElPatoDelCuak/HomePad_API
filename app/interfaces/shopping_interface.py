from typing import Protocol, List, Optional
from app.schemas.shopping_schema import ShoppingCreate, ShoppingUpdate
from app.models.entities.shopping_entity import ShoppingEntity

class IShoppingRepository(Protocol):
    def get_all(self) -> List[ShoppingEntity]:
        ...

    def get_by_id(self, item_id: int) -> Optional[ShoppingEntity]:
        ...

    def get_picked_items(self) -> List[ShoppingEntity]:
        ...

    def create(self, item_data: ShoppingCreate) -> ShoppingEntity:
        ...

    def update(self, item_id: int, item_data: ShoppingUpdate) -> Optional[ShoppingEntity]:
        ...

    def delete(self, item_id: int) -> bool:
        ...

    def delete_many(self, item_ids: List[int]) -> bool:
        ...