from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.entities.product_entity import ProductEntity
from app.schemas.product_schema import ProductCreate, ProductUpdate


class ProductRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_all(self) -> list[ProductEntity]:
        stmt = select(ProductEntity).order_by(ProductEntity.id.asc())
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, product_id: int) -> ProductEntity | None:
        stmt = select(ProductEntity).where(ProductEntity.id == product_id)
        return self.db.scalars(stmt).first()

    def get_by_name(self, name: str) -> ProductEntity | None:
        stmt = select(ProductEntity).where(ProductEntity.name == name)
        return self.db.scalars(stmt).first()

    def create(self, product_data: ProductCreate) -> ProductEntity:
        entity = ProductEntity(
            name=product_data.name,
            category=product_data.category,
            unit=product_data.unit,
        )
        self.db.add(entity)
        self.db.commit()
        self.db.refresh(entity)
        return entity

    def update(self, product_id: int, product_data: ProductUpdate) -> ProductEntity | None:
        entity = self.get_by_id(product_id)
        if not entity:
            return None

        update_dict = product_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(entity, key, value)

        self.db.commit()
        self.db.refresh(entity)
        return entity

    def delete(self, product_id: int) -> bool:
        entity = self.get_by_id(product_id)
        if not entity:
            return False

        self.db.delete(entity)
        self.db.commit()
        return True
