from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

# Esquema base con campos comunes
class ProductBase(BaseModel):
    name: str
    category: Optional[str] = None
    unit: str = "unidades"

# Para crear un producto (POST)
class ProductCreate(ProductBase):
    pass

# Para actualizar un producto (PUT/PATCH)
class ProductUpdate(BaseModel):
    name: Optional[str] = None
    category: Optional[str] = None
    unit: Optional[str] = None

# Para devolver en la respuesta de la API (GET)
class ProductResponse(ProductBase):
    id: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)