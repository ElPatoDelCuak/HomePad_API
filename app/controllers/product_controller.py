from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_product_service
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate
from app.services.product_service import ProductService


router = APIRouter(prefix="/products", tags=["products"])


@router.get("/", response_model=List[ProductResponse])
def get_products(service: ProductService = Depends(get_product_service)):
    return service.get_all()


@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, service: ProductService = Depends(get_product_service)):
    product = service.get_by_id(product_id)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.post("/", response_model=ProductResponse, status_code=status.HTTP_201_CREATED)
def create_product(
    product_data: ProductCreate,
    service: ProductService = Depends(get_product_service),
):
    return service.create(product_data)


@router.patch("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_data: ProductUpdate,
    service: ProductService = Depends(get_product_service),
):
    product = service.update(product_id, product_data)
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, service: ProductService = Depends(get_product_service)):
    if not service.delete(product_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product not found")