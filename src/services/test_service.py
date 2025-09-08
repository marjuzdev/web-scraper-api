from repositories.test_repository import TestRepository
from schemas.test import TestSchema
from motor.motor_asyncio import AsyncIOMotorDatabase

class TestService:
    
    def __init__(self, db: AsyncIOMotorDatabase = None ):
        self.repository = TestRepository(db)
    
    async def get_all(self):
        return await self.repository.get_all()
    
    async def save( self, test: TestSchema ):
        test_dict = test.model_dump()
        test_dict["url_base"] = str(test_dict["url_base"])
        return await self.repository.save(test_dict)
    
    async def delete( self, test_id: str ):
        return await self.repository.delete(test_id)
    
    async def update( self, test_id: str, test: TestSchema):
        test_dict = test.model_dump(exclude_unset=True)
        return await self.repository.update(test_id, test_dict )