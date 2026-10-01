from fastapi import HTTPException, status
from app.interfaces.inventory_interface import InventoryRepositoryProtocol
from app.interfaces.product_interface import ProductRepositoryProtocol
from app.interfaces.shopping_interface import ShoppingRepositoryProtocol
from app.schemas.shopping_schema import (
    CheckoutSummaryResponse,
    ShoppingItemCreate,
    ShoppingItemUpdate,
    ShoppingWithProductResponse,
)


class ShoppingService:
    def __init__(
        self,
        shopping_repo: ShoppingRepositoryProtocol,
        inventory_repo: InventoryRepositoryProtocol,
        product_repo: ProductRepositoryProtocol,
    ) -> None:
        self.shopping_repo = shopping_repo
        self.inventory_repo = inventory_repo
        self.product_repo = product_repo

    def get_all_shopping_items(self) -> list[ShoppingWithProductResponse]:
        entities = self.shopping_repo.get_all()
        return [ShoppingWithProductResponse.model_validate(e) for e in entities]

    def get_shopping_item_by_id(self, item_id: int) -> ShoppingWithProductResponse:
        entity = self.shopping_repo.get_by_id(item_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shopping item with id {item_id} not found"
            )
        return ShoppingWithProductResponse.model_validate(entity)

    def create_shopping_item(self, shopping_data: ShoppingItemCreate) -> ShoppingWithProductResponse:
        product = self.product_repo.get_by_id(shopping_data.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {shopping_data.product_id} not found"
            )

        existing = self.shopping_repo.get_by_product_id(shopping_data.product_id)
        if existing:
            new_quantity = existing.quantity + shopping_data.quantity
            update_dto = ShoppingItemUpdate(quantity=new_quantity, is_picked=shopping_data.is_picked)
            updated_entity = self.shopping_repo.update(existing.id, update_dto)
            return ShoppingWithProductResponse.model_validate(updated_entity)

        entity = self.shopping_repo.create(shopping_data)
        return ShoppingWithProductResponse.model_validate(entity)

    def update_shopping_item(self, item_id: int, shopping_data: ShoppingItemUpdate) -> ShoppingWithProductResponse:
        entity = self.shopping_repo.update(item_id, shopping_data)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shopping item with id {item_id} not found"
            )
        return ShoppingWithProductResponse.model_validate(entity)

    def delete_shopping_item(self, item_id: int) -> None:
        success = self.shopping_repo.delete(item_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Shopping item with id {item_id} not found"
            )

    def checkout(self) -> CheckoutSummaryResponse:
        """
        Process checkout flow for picked shopping list items:
        1. Fetch all items in shopping_list with is_picked == True.
        2. For each picked item:
           - If product exists in inventory, add quantity.
           - If not in inventory, create new inventory record.
        3. Remove processed items from shopping_list.
        """
        picked_items = self.shopping_repo.get_picked_items()

        if not picked_items:
            return CheckoutSummaryResponse(
                processed_items_count=0,
                message="No picked items found in shopping list to checkout.",
                processed_items=[]
            )

        processed_dtos: list[ShoppingWithProductResponse] = []
        item_ids_to_delete: list[int] = []

        for item in picked_items:
            self.inventory_repo.add_quantity(
                product_id=item.product_id,
                quantity=item.quantity
            )

            processed_dtos.append(ShoppingWithProductResponse.model_validate(item))
            item_ids_to_delete.append(item.id)

        self.shopping_repo.delete_items(item_ids_to_delete)

        return CheckoutSummaryResponse(
            processed_items_count=len(processed_dtos),
            message=f"Successfully processed {len(processed_dtos)} item(s) into inventory.",
            processed_items=processed_dtos
        )
