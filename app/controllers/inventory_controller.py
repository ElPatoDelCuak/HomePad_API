from fastapi import APIRouter, Depends, status

from app.dependencies import get_inventory_service
from app.schemas.inventory_schema import (
    InventoryCreate,
    InventoryUpdate,
    InventoryWithProductResponse,
)
from app.services.inventory_service import InventoryService

router = APIRouter(prefix="/inventory", tags=["Inventory"])


@router.get("/", response_model=list[InventoryWithProductResponse], status_code=status.HTTP_200_OK)
def get_inventory(
    service: InventoryService = Depends(get_inventory_service),
) -> list[InventoryWithProductResponse]:
    return service.get_all_inventory()


@router.get("/{item_id}", response_model=InventoryWithProductResponse, status_code=status.HTTP_200_OK)
def get_inventory_item(
    item_id: int,
    service: InventoryService = Depends(get_inventory_service),
) -> InventoryWithProductResponse:
    return service.get_inventory_item_by_id(item_id)


@router.post("/", response_model=InventoryWithProductResponse, status_code=status.HTTP_201_CREATED)
def create_inventory_item(
    inventory_data: InventoryCreate,
    service: InventoryService = Depends(get_inventory_service),
) -> InventoryWithProductResponse:
    return service.create_inventory_item(inventory_data)


@router.put("/{item_id}", response_model=InventoryWithProductResponse, status_code=status.HTTP_200_OK)
def update_inventory_item(
    item_id: int,
    inventory_data: InventoryUpdate,
    service: InventoryService = Depends(get_inventory_service),
) -> InventoryWithProductResponse:
    return service.update_inventory_item(item_id, inventory_data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_inventory_item(
    item_id: int,
    service: InventoryService = Depends(get_inventory_service),
) -> None:
    service.delete_inventory_item(item_id)
