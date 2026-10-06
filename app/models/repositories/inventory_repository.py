from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.entities.inventory_entity import InventoryEntity
from app.schemas.inventory_schema import InventoryCreate, InventoryUpdate

class InventoryRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[InventoryEntity]:
        stmt = select(InventoryEntity)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, item_id: int) -> Optional[InventoryEntity]:
        return self.db.get(InventoryEntity, item_id)

    def get_by_product_id(self, product_id: int) -> Optional[InventoryEntity]:
        stmt = select(InventoryEntity).where(InventoryEntity.product_id == product_id)
        return self.db.scalars(stmt).first()

    def create(self, item_data: InventoryCreate) -> InventoryEntity:
        db_item = InventoryEntity(**item_data.model_dump())
        self.db.add(db_item)
        self.db.commit()
        self.db.refresh(db_item)
        return db_item

    def update(self, item_id: int, item_data: InventoryUpdate) -> Optional[InventoryEntity]:
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