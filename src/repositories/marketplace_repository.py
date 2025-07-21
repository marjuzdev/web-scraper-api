from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId, errors

from schemas.marketplace import MarketplaceSchema

class MarketPlaceRepository:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["marketplaces"]

    async def save(self, marketplace: dict):
        try:
            result = await self.collection.insert_one(marketplace)
            return str(result.inserted_id)

        except Exception as error:
            print(f"Error: {error}")
            raise HTTPException(status_code=500, detail="Error al crear tienda")
        
   
    async def get_all(self):
        try:

            marketplaces = await self.collection.find().to_list(length=100)
            return marketplaces


        except Exception as error:
            print(f"Get all marketplaces: {error}")
            raise HTTPException(status_code=500, detail="Error al listar tiendas")


    


