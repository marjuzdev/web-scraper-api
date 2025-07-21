from repositories.marketplace_repository import MarketPlaceRepository
from schemas.marketplace import MarketplaceSchema

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