from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict
from app.schemas.product_schema import ProductResponse

class ShoppingBase(BaseModel):
    product_id: int
    quantity: float = 1.00
    is_picked: bool = False

class ShoppingCreate(ShoppingBase):
    pass

class ShoppingUpdate(BaseModel):
    quantity: Optional[float] = None
    is_picked: Optional[bool] = None

class ShoppingResponse(ShoppingBase):
    id: int
    created_at: datetime
    product: Optional[ProductResponse] = None

    model_config = ConfigDict(from_attributes=True)