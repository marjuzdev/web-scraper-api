from repositories.product_repository import ProductRepository
from schemas.product import ProductSchema

class ProductService:
    def __init__(self, repository: ProductRepository):
        self.repository = repository

    async def create_product(self, product: ProductSchema):
        
        product_dict = product.model_dump()
        return await self.repository.save(product_dict)
