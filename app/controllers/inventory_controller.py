from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.dependencies import get_inventory_service
from app.schemas.inventory_schema import InventoryCreate, InventoryResponse, InventoryUpdate
from app.services.inventory_service import InventoryService


router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("/", response_model=List[InventoryResponse])
def get_inventory(service: InventoryService = Depends(get_inventory_service)):
    return service.get_all()


@router.get("/product/{product_id}", response_model=InventoryResponse)
def get_inventory_by_product(
    product_id: int,
    service: InventoryService = Depends(get_inventory_service),
):
    item = service.get_by_product_id(product_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")
    return item


@router.get("/{item_id}", response_model=InventoryResponse)
def get_inventory_item(item_id: int, service: InventoryService = Depends(get_inventory_service)):
    item = service.get_by_id(item_id)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")
    return item


@router.post("/", response_model=InventoryResponse, status_code=status.HTTP_201_CREATED)
def create_inventory_item(
    item_data: InventoryCreate,
    service: InventoryService = Depends(get_inventory_service),
):
    return service.create(item_data)


@router.patch("/{item_id}", response_model=InventoryResponse)
def update_inventory_item(
    item_id: int,
    item_data: InventoryUpdate,
    service: InventoryService = Depends(get_inventory_service),
):
    item = service.update(item_id, item_data)
    if not item:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")
    return item


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_item(item_id: int, service: InventoryService = Depends(get_inventory_service)):
    if not service.delete(item_id):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Inventory item not found")