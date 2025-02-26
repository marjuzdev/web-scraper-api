from repositories.product_repository import ProductRepository
from schemas.product import ProductSchema

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def create_product(self, product: ProductSchema):
        product_dict = product.model_dump()
        return await self.repository.save(product_dict)
    

    async def get_product(self, product_id: str):
        return await self.repository.get_product(product_id)

