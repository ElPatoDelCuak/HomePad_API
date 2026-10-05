from datetime import datetime, date
from typing import Optional
from sqlalchemy import Numeric, Date, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class InventoryEntity(Base):
    __tablename__ = "inventory"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), 
        nullable=False
    )
    quantity: Mapped[float] = mapped_column(Numeric(10, 2), server_default="1.00", nullable=False)
    expiration_date: Mapped[Optional[date]] = mapped_column(Date, nullable=True)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )

    # Relación con Producto
    product: Mapped["ProductEntity"] = relationship("ProductEntity", back_populates="inventory_items")