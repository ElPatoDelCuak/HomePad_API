from datetime import datetime
from typing import TYPE_CHECKING
from sqlalchemy import DateTime, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base

if TYPE_CHECKING:
    from app.models.entities.inventory_entity import InventoryEntity
    from app.models.entities.shopping_entity import ShoppingItemEntity


class ProductEntity(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False, unique=True)
    category: Mapped[str | None] = mapped_column(String(50), nullable=True)
    unit: Mapped[str] = mapped_column(String(20), nullable=False, server_default="unidades")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now()
    )

    # Relationships
    inventory_items: Mapped[list["InventoryEntity"]] = relationship(
        "InventoryEntity",
        back_populates="product",
        cascade="all, delete-orphan"
    )
    shopping_items: Mapped[list["ShoppingItemEntity"]] = relationship(
        "ShoppingItemEntity",
        back_populates="product",
        cascade="all, delete-orphan"
    )
