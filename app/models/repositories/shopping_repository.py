from sqlalchemy import delete, select
from sqlalchemy.orm import Session, joinedload

from app.models.entities.shopping_entity import ShoppingItemEntity
from app.schemas.shopping_schema import ShoppingItemCreate, ShoppingItemUpdate


class ShoppingRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[ShoppingItemEntity]:
        stmt = (
            select(ShoppingItemEntity)
            .options(joinedload(ShoppingItemEntity.product))
            .order_by(ShoppingItemEntity.id.asc())
        )
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, item_id: int) -> ShoppingItemEntity | None:
        stmt = (
            select(ShoppingItemEntity)
            .options(joinedload(ShoppingItemEntity.product))
            .where(ShoppingItemEntity.id == item_id)
        )
        return self.db.scalars(stmt).first()

    def get_by_product_id(self, product_id: int) -> ShoppingItemEntity | None:
        stmt = (
            select(ShoppingItemEntity)
            .options(joinedload(ShoppingItemEntity.product))
            .where(ShoppingItemEntity.product_id == product_id)
        )
        return self.db.scalars(stmt).first()

    def get_picked_items(self) -> list[ShoppingItemEntity]:
        stmt = (
            select(ShoppingItemEntity)
            .options(joinedload(ShoppingItemEntity.product))
            .where(ShoppingItemEntity.is_picked.is_(True))
        )
        return list(self.db.scalars(stmt).all())

    def create(self, shopping_data: ShoppingItemCreate) -> ShoppingItemEntity:
        entity = ShoppingItemEntity(
            product_id=shopping_data.product_id,
            quantity=shopping_data.quantity,
            is_picked=shopping_data.is_picked,
        )
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return self.get_by_id(entity.id) or entity

    def update(self, item_id: int, shopping_data: ShoppingItemUpdate) -> ShoppingItemEntity | None:
        entity = self.db.scalars(
            select(ShoppingItemEntity).where(ShoppingItemEntity.id == item_id)
        ).first()
        if not entity:
            return None

        update_dict = shopping_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(entity, key, value)

        self.db.commit()
        return self.get_by_id(item_id)

    def delete(self, item_id: int) -> bool:
        entity = self.db.scalars(
            select(ShoppingItemEntity).where(ShoppingItemEntity.id == item_id)
        ).first()
        if not entity:
            return False

        self.db.delete(entity)
        self.db.commit()
        return True

    def delete_items(self, item_ids: list[int]) -> None:
        if not item_ids:
            return
        stmt = delete(ShoppingItemEntity).where(ShoppingItemEntity.id.in_(item_ids))
        self.db.execute(stmt)
        self.db.commit()
