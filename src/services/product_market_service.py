from repositories.product_market_repository import ProductMarketRepository
from schemas.product_market import ProductMarketCreateSchema, ProductMarketUpdateSchema, ProductMarketFilterSchema
from motor.motor_asyncio import AsyncIOMotorDatabase

class ProductMarketService:
    
    def __init__(self, db: AsyncIOMotorDatabase = None ):
        self.repository = ProductMarketRepository(db)
    
    async def save( self, test: ProductMarketCreateSchema ):
        test_dict = test.model_dump()
        test_dict["url_base"] = str(test_dict["url_base"])
        return await self.repository.save(test_dict)
    
    async def get_by_id( self, test_id: str ):
        return await self.repository.get_by_id(test_id)
    
    async def get_all(self):
        return await self.repository.get_all()
    
    async def get_by_market(self, marketplace_id):
        return await self.repository.get_by_market(marketplace_id)
    
    async def get_products_by_marketplace_agg(self, marketplace_id):
        return await self.repository.get_products_by_marketplace_agg(marketplace_id)
    
    async def delete( self, test_id: str ):
        return await self.repository.delete(test_id)
    
    async def update( self, test_id: str, test: ProductMarketUpdateSchema):
        test_dict = test.model_dump(exclude_unset=True)
        return await self.repository.update(test_id, test_dict )
    
    async def raw_find( self, filters: ProductMarketFilterSchema):
        filters = filters.model_dump(exclude_unset=True)

        limit = filters['limit']
        return await self.repository.raw_find(filters, limit)