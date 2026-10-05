from datetime import datetime, date
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.product_schema import ProductResponse

class InventoryBase(BaseModel):
    product_id: int
    quantity: float = 1.00
    expiration_date: Optional[date] = None

class InventoryCreate(InventoryBase):
    pass

class InventoryUpdate(BaseModel):
    quantity: Optional[float] = None
    expiration_date: Optional[date] = None

class InventoryResponse(InventoryBase):
    id: int
    updated_at: datetime
    product: Optional[ProductResponse] = None  # Anida los datos del producto relacionado

    model_config = ConfigDict(from_attributes=True)