from fastapi import APIRouter, Depends, status

from app.dependencies import get_shopping_service
from app.schemas.shopping_schema import (
    CheckoutSummaryResponse,
    ShoppingItemCreate,
    ShoppingItemUpdate,
    ShoppingWithProductResponse,
)
from app.services.shopping_service import ShoppingService

router = APIRouter(prefix="/shopping-list", tags=["Shopping List"])


@router.get("/", response_model=list[ShoppingWithProductResponse], status_code=status.HTTP_200_OK)
def get_shopping_list(
    service: ShoppingService = Depends(get_shopping_service),
) -> list[ShoppingWithProductResponse]:
    return service.get_all_shopping_items()


@router.get("/{item_id}", response_model=ShoppingWithProductResponse, status_code=status.HTTP_200_OK)
def get_shopping_item(
    item_id: int,
    service: ShoppingService = Depends(get_shopping_service),
) -> ShoppingWithProductResponse:
    return service.get_shopping_item_by_id(item_id)


@router.post("/", response_model=ShoppingWithProductResponse, status_code=status.HTTP_201_CREATED)
def create_shopping_item(
    shopping_data: ShoppingItemCreate,
    service: ShoppingService = Depends(get_shopping_service),
) -> ShoppingWithProductResponse:
    return service.create_shopping_item(shopping_data)


@router.put("/{item_id}", response_model=ShoppingWithProductResponse, status_code=status.HTTP_200_OK)
def update_shopping_item(
    item_id: int,
    shopping_data: ShoppingItemUpdate,
    service: ShoppingService = Depends(get_shopping_service),
) -> ShoppingWithProductResponse:
    return service.update_shopping_item(item_id, shopping_data)


@router.delete("/{item_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_shopping_item(
    item_id: int,
    service: ShoppingService = Depends(get_shopping_service),
) -> None:
    service.delete_shopping_item(item_id)


@router.post("/checkout", response_model=CheckoutSummaryResponse, status_code=status.HTTP_200_OK)
def checkout_shopping_list(
    service: ShoppingService = Depends(get_shopping_service),
) -> CheckoutSummaryResponse:
    return service.checkout()
