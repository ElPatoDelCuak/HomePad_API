from fastapi import HTTPException, status
from app.interfaces.product_interface import ProductRepositoryProtocol
from app.schemas.product_schema import ProductCreate, ProductResponse, ProductUpdate


class ProductService:
    def __init__(self, product_repo: ProductRepositoryProtocol) -> None:
        self.product_repo = product_repo

    def get_all_products(self) -> list[ProductResponse]:
        entities = self.product_repo.get_all()
        return [ProductResponse.model_validate(e) for e in entities]

    def get_product_by_id(self, product_id: int) -> ProductResponse:
        entity = self.product_repo.get_by_id(product_id)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        return ProductResponse.model_validate(entity)

    def create_product(self, product_data: ProductCreate) -> ProductResponse:
        existing = self.product_repo.get_by_name(product_data.name)
        if existing:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with name '{product_data.name}' already exists"
            )
        entity = self.product_repo.create(product_data)
        return ProductResponse.model_validate(entity)

    def update_product(self, product_id: int, product_data: ProductUpdate) -> ProductResponse:
        if product_data.name:
            existing = self.product_repo.get_by_name(product_data.name)
            if existing and existing.id != product_id:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product with name '{product_data.name}' already exists"
                )

        entity = self.product_repo.update(product_id, product_data)
        if not entity:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
        return ProductResponse.model_validate(entity)

    def delete_product(self, product_id: int) -> None:
        success = self.product_repo.delete(product_id)
        if not success:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Product with id {product_id} not found"
            )
