from datetime import datetime
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field

from app.schemas.product_schema import ProductResponse


class ShoppingItemBase(BaseModel):
    product_id: int = Field(..., description="ID of the product to purchase")
    quantity: Decimal = Field(default=Decimal("1.00"), gt=Decimal("0"), decimal_places=2, max_digits=10)
    is_picked: bool = Field(default=False, description="Flag indicating if the item was picked in cart")


class ShoppingItemCreate(ShoppingItemBase):
    pass


class ShoppingItemUpdate(BaseModel):
    quantity: Decimal | None = Field(default=None, decimal_places=2, max_digits=10)
    is_picked: bool | None = Field(default=None)


class ShoppingItemResponse(ShoppingItemBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ShoppingWithProductResponse(ShoppingItemResponse):
    product: ProductResponse

    model_config = ConfigDict(from_attributes=True)


class CheckoutSummaryResponse(BaseModel):
    processed_items_count: int
    message: str
    processed_items: list[ShoppingWithProductResponse]
