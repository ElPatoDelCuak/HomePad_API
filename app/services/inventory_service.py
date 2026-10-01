from fastapi import HTTPException, status
from app.interfaces.inventory_interface import InventoryRepositoryProtocol
from app.interfaces.product_interface import ProductRepositoryProtocol
from app.schemas.inventory_schema import (
    InventoryCreate,
    InventoryUpdate,
    InventoryWithProductResponse,
)


class InventoryService:
    def __init__(
        self,
        inventory_repo: InventoryRepositoryProtocol,
        product_repo: ProductRepositoryProtocol,
    ) -> None:
        self.inventory_repo = inventory_repo
        self.product_repo = product_repo

    def get_all_inventory(self) -> list[InventoryWithProductResponse]:
        entities = self.inventory_repo.get_all()
        return [InventoryWithProductResponse.model_validate(e) for e in entities]

    def get_inventory_item_by_id(self, item_id: int) -> InventoryWithProductResponse:
        entity = self.inventory_repo.get_by_id(item_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventory item with id {item_id} not found"
            )
        return InventoryWithProductResponse.model_validate(entity)

    def create_inventory_item(self, inventory_data: InventoryCreate) -> InventoryWithProductResponse:
        product = self.product_repo.get_by_id(inventory_data.product_id)
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {inventory_data.product_id} not found"
            )

        existing = self.inventory_repo.get_by_product_id(inventory_data.product_id)
        if existing:
            updated_entity = self.inventory_repo.add_quantity(
                product_id=inventory_data.product_id,
                quantity=inventory_data.quantity,
            )
            return InventoryWithProductResponse.model_validate(updated_entity)

        entity = self.inventory_repo.create(inventory_data)
        return InventoryWithProductResponse.model_validate(entity)

    def update_inventory_item(self, item_id: int, inventory_data: InventoryUpdate) -> InventoryWithProductResponse:
        entity = self.inventory_repo.update(item_id, inventory_data)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventory item with id {item_id} not found"
            )
        return InventoryWithProductResponse.model_validate(entity)

    def delete_inventory_item(self, item_id: int) -> None:
        success = self.inventory_repo.delete(item_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Inventory item with id {item_id} not found"
            )
