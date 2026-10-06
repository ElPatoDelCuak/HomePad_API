from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select, delete
from app.models.entities.shopping_entity import ShoppingEntity
from app.schemas.shopping_schema import ShoppingCreate, ShoppingUpdate

class ShoppingRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ShoppingEntity]:
        stmt = select(ShoppingEntity)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, item_id: int) -> Optional[ShoppingEntity]:
        return self.db.get(ShoppingEntity, item_id)

    def get_picked_items(self) -> List[ShoppingEntity]:
        stmt = select(ShoppingEntity).where(ShoppingEntity.is_picked == True)
        return list(self.db.scalars(stmt).all())

    def create(self, item_data: ShoppingCreate) -> ShoppingEntity:
        db_item = ShoppingEntity(**item_data.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, item_id: int, item_data: ShoppingUpdate) -> Optional[ShoppingEntity]:
        db_item = self.get_by_id(item_id)
        if not db_item:
            return None

        update_dict = item_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_item, key, value)

        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def delete(self, item_id: int) -> bool:
        db_item = self.get_by_id(item_id)
        if not db_item:
            return False

        self.db.delete(db_item)
        self.db.commit()
        return True

    def delete_many(self, item_ids: List[int]) -> bool:
        if not item_ids:
            return True

        stmt = delete(ShoppingEntity).where(ShoppingEntity.id.in_(item_ids))
        self.db.execute(stmt)
        self.db.commit()
        return True