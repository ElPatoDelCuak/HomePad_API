from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field


class ProductBase(BaseModel):
    name: str = Field(..., max_length=100, description="Unique product name")
    category: str | None = Field(default=None, max_length=50, description="Product category")
    unit: str = Field(default="unidades", max_length=20, description="Unit of measurement")


class ProductCreate(ProductBase):
    pass


class ProductUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    category: str | None = Field(default=None, max_length=50)
    unit: str | None = Field(default=None, max_length=20)


class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
