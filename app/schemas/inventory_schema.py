from datetime import date, datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.product_schema import ProductResponse


class InventoryBase(BaseModel):
    product_id: int = Field(..., description="ID of the related product")
    quantity: Decimal = Field(default=Decimal("1.00"), ge=Decimal("0"), decimal_places=2, max_digits=10)
    expiration_date: date | None = Field(default=None, description="Expiration date")


class InventoryCreate(InventoryBase):
    pass


class InventoryUpdate(BaseModel):
    quantity: Decimal | None = Field(default=None, decimal_places=2, max_digits=10)
    expiration_date: date | None = Field(default=None)


class InventoryResponse(InventoryBase):
    id: int
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class InventoryWithProductResponse(InventoryResponse):
    product: ProductResponse

    model_config = ConfigDict(from_attributes=True)
