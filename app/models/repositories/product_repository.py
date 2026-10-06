from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.entities.product_entity import ProductEntity
from app.schemas.product_schema import ProductCreate, ProductUpdate

class ProductRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_all(self) -> List[ProductEntity]:
        stmt = select(ProductEntity)
        return list(self.db.scalars(stmt).all())

    def get_by_id(self, product_id: int) -> Optional[ProductEntity]:
        return self.db.get(ProductEntity, product_id)

    def get_by_name(self, name: str) -> Optional[ProductEntity]:
        stmt = select(ProductEntity).where(ProductEntity.name == name)
        return self.db.scalars(stmt).first()

    def create(self, product_data: ProductCreate) -> ProductEntity:
        db_product = ProductEntity(**product_data.model_dump())
        self.db.add(db_product)
        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def update(self, product_id: int, product_data: ProductUpdate) -> Optional[ProductEntity]:
        db_product = self.get_by_id(product_id)
        if not db_product:
            return None

        update_dict = product_data.model_dump(exclude_unset=True)
        for key, value in update_dict.items():
            setattr(db_product, key, value)

        self.db.commit()
        self.db.refresh(db_product)
        return db_product

    def delete(self, product_id: int) -> bool:
        db_product = self.get_by_id(product_id)
        if not db_product:
            return False

        self.db.delete(db_product)
        self.db.commit()
        return True