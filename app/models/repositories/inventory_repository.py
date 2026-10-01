from decimal import Decimal
from sqlalchemy import select
from sqlalchemy.orm import Session, joinedload

from app.models.entities.inventory_entity import InventoryEntity
from app.schemas.inventory_schema import InventoryCreate, InventoryUpdate


class InventoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[InventoryEntity]:
        stmt = (
            select(InventoryEntity)
            .options(joinedload(InventoryEntity.product))
            .order_by(InventoryEntity.id.asc())
        )
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, item_id: int) -> InventoryEntity | None:
        stmt = (
            select(InventoryEntity)
            .options(joinedload(InventoryEntity.product))
            .where(InventoryEntity.id == item_id)
        )
        return self.db.scalars(stmt).first()

    def get_by_product_id(self, product_id: int) -> InventoryEntity | None:
        stmt = (
            select(InventoryEntity)
            .options(joinedload(InventoryEntity.product))
            .where(InventoryEntity.product_id == product_id)
        )
        return self.db.scalars(stmt).first()

    def create(self, inventory_data: InventoryCreate) -> InventoryEntity:
        entity = InventoryEntity(
            product_id=inventory_data.product_id,
            quantity=inventory_data.quantity,
            expiration_date=inventory_data.expiration_date,
        )
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return self.get_by_id(entity.id) or entity

    def update(self, item_id: int, inventory_data: InventoryUpdate) -> InventoryEntity | None:
        entity = self.db.scalars(
            select(InventoryEntity).where(InventoryEntity.id == item_id)
        ).first()
        if not entity:
            return None

        update_dict = inventory_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(entity, key, value)

        self.db.commit()
        return self.get_by_id(item_id)

    def add_quantity(self, product_id: int, quantity: Decimal) -> InventoryEntity:
        entity = self.db.scalars(
            select(InventoryEntity).where(InventoryEntity.product_id == product_id)
        ).first()

        if entity:
            entity.quantity += quantity
        else:
            entity = InventoryEntity(
                product_id=product_id,
                quantity=quantity
            )
            self.db.add(entity)

        self.db.commit()
        return self.get_by_id(entity.id) or entity

    def delete(self, item_id: int) -> bool:
        entity = self.db.scalars(
            select(InventoryEntity).where(InventoryEntity.id == item_id)
        ).first()
        if not entity:
            return False

        self.db.delete(entity)
        self.db.commit()
        return True
