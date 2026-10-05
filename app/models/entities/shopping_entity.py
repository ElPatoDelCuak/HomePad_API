from datetime import datetime
from sqlalchemy import Numeric, Boolean, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from app.database import Base

class ShoppingEntity(Base):
    __tablename__ = "shopping_list"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), 
        nullable=False
    )
    quantity: Mapped[float] = mapped_column(Numeric(10, 2), server_default="1.00", nullable=False)
    is_picked: Mapped[bool] = mapped_column(Boolean, server_default="false", nullable=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        nullable=False
    )

    # Relación con Producto
    product: Mapped["ProductEntity"] = relationship("ProductEntity", back_populates="shopping_items")