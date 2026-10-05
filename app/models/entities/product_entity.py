from datetime import datetime
from typing import Optional
from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class ProductEntity(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)
    category: Mapped[Optional[str]] = mapped_column(String(50), nullable=True)
    unit: Mapped[str] = mapped_column(String(20), server_default="unidades", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )

    # Relaciones ORM
    inventory_items: Mapped[list["InventoryEntity"]] = relationship(
        "InventoryEntity", 
        back_populates="product", 
        cascade="all, delete-orphan"
    )
    shopping_items: Mapped[list["ShoppingEntity"]] = relationship(
        "ShoppingEntity", 
        back_populates="product", 
        cascade="all, delete-orphan"
    )