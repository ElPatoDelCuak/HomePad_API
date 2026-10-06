from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_shopping_service
from app.schemas.shopping_schema import ShoppingCreate, ShoppingResponse, ShoppingUpdate
from app.services.shopping_service import ShoppingService


router = APIRouter(prefix="/shopping", tags=["shopping"])


@router.get("/", response_model=List[ShoppingResponse])
def get_shopping_items(service: ShoppingService = Depends(get_shopping_service)):
    return service.get_all()


@router.get("/picked", response_model=List[ShoppingResponse])
def get_picked_items(service: ShoppingService = Depends(get_shopping_service)):
    return service.get_picked_items()


@router.get("/{item_id}", response_model=ShoppingResponse)
def get_shopping_item(item_id: int, service: ShoppingService = Depends(get_shopping_service)):
    item = service.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shopping item not found")
    return item


@router.post("/", response_model=ShoppingResponse, status_code=status.HTTP_201_CREATED)
def create_shopping_item(
    item_data: ShoppingCreate,
    service: ShoppingService = Depends(get_shopping_service),
):
    return service.create(item_data)


@router.patch("/{item_id}", response_model=ShoppingResponse)
def update_shopping_item(
    item_id: int,
    item_data: ShoppingUpdate,
    service: ShoppingService = Depends(get_shopping_service),
):
    item = service.update(item_id, item_data)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shopping item not found")
    return item


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT)
def delete_shopping_items(
    item_ids: List[int],
    service: ShoppingService = Depends(get_shopping_service),
):
    service.delete_many(item_ids)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shopping_item(item_id: int, service: ShoppingService = Depends(get_shopping_service)):
    if not service.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Shopping item not found")