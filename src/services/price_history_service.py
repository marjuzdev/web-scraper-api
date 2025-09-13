from repositories.price_history_repository import PriceHistoryRepository
from schemas.price_history import PriceHistoryCreateSchema, PriceHistoryFilterSchema, PriceHistoryUpdateSchema
from motor.motor_asyncio import AsyncIOMotorDatabase

class PriceHistoryService:
    
    def __init__(self, db: AsyncIOMotorDatabase = None ):
        self.repository = PriceHistoryRepository(db)
    
    async def save( self, test: PriceHistoryCreateSchema ):
        test_dict = test.model_dump()
        test_dict["url_base"] = str(test_dict["url_base"])
        return await self.repository.save(test_dict)
    
    async def get_by_id( self, test_id: str ):
        return await self.repository.get_by_id(test_id)
    
    async def get_all(self):
        return await self.repository.get_all()
    
    async def delete( self, test_id: str ):
        return await self.repository.delete(test_id)
    
    async def update( self, test_id: str, test: PriceHistoryUpdateSchema):
        test_dict = test.model_dump(exclude_unset=True)
        return await self.repository.update(test_id, test_dict )
    
    async def raw_find( self, filters: PriceHistoryFilterSchema):
        filters = filters.model_dump(exclude_unset=True)

        limit = filters['limit']
        return await self.repository.raw_find(filters, limit)