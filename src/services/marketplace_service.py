from repositories.marketplace_repository import MarketPlaceRepository
from schemas.marketplace import MarketplaceSchema, MarketplaceUpdateSchema

class MarketplaceService:
    def __init__(self, db ):
        self.repository = MarketPlaceRepository(db)
    
    async def get_all(self):
        return await self.repository.get_all()
       
    async def save(
        self,
        marketplace: MarketplaceSchema
    ):
        marketplace_dict = marketplace.model_dump()
        return await self.repository.save(marketplace_dict)
    
    async def delete(
        self,
        marketplace_id: str
    ):
        return await self.repository.delete(marketplace_id)
    
    async def update(
        self,
        marketplace_id: str,
        marketplace: MarketplaceUpdateSchema
    ):
        marketplace_dict = marketplace.model_dump(exclude_unset=True)
        return await self.repository.update(marketplace_id, marketplace_dict )