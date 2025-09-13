from repositories.product_repository import ProductRepository
from schemas.product import ProductSchema

class ProductService:

    def __init__(self, db ):
        self.repository = ProductRepository(db)

    async def create_product(self, product: ProductSchema):
        product_dict = product.model_dump()
        return await self.repository.save(product_dict)
    

    async def get_product(self, product_id: str):
        return await self.repository.get_product(product_id)
    
    async def get_all(self):
        return await self.repository.get_all()

