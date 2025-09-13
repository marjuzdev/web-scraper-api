from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId
from logger import configure_logger

logger = configure_logger()

class MarketPlaceRepository:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["marketplaces"]

    async def save(self, marketplace: dict):
        try:
            existing = await self.collection.find_one({"name": marketplace.get("name")})
            if existing:
                raise HTTPException(status_code=400, detail="Marketplace name already exists")

            result = await self.collection.insert_one(marketplace)
            return str(result.inserted_id)

        except HTTPException:
            raise
        except Exception:
            logger.exception("Unexpected error while saving marketplace")
            raise HTTPException(status_code=500, detail="Failed to create marketplace")

    async def get_all(self):
        try:
            docs = await self.collection.find().to_list(length=100)
            return [
                {**doc, "_id": str(doc["_id"])} 
                if "_id" in doc and isinstance(doc["_id"], ObjectId) else doc
                for doc in docs
            ]
        
        except Exception:
            logger.exception("Unexpected error while listing marketplaces")
            raise HTTPException(status_code=500, detail="Failed to list marketplaces")

    async def get_by_id(self, marketplace_id: str):
        try:
            if not ObjectId.is_valid(marketplace_id):
                raise HTTPException(status_code=400, detail="Invalid ID format")

            marketplace = await self.collection.find_one({"_id": ObjectId(marketplace_id)})
            if not marketplace:
                raise HTTPException(status_code=404, detail="Marketplace not found")
            return marketplace

        except HTTPException:
            raise
        except Exception:
            logger.exception("Unexpected error while retrieving marketplace by ID")
            raise HTTPException(status_code=500, detail="Failed to retrieve marketplace")

    async def update(self, marketplace_id: str, update_data: dict):
            try:
                if not ObjectId.is_valid(marketplace_id):
                    raise HTTPException(status_code=400, detail="Invalid ID format")

                result = await self.collection.update_one(
                    {"_id": ObjectId(marketplace_id)},
                    {"$set": update_data}
                )

                if result.matched_count == 0:
                    raise HTTPException(status_code=404, detail="Marketplace not found")

                return {"updated": True}

            except HTTPException as e:
                logger.error(f"HTTPException: {e.detail}")
                raise e
            except Exception as e:
                logger.exception(f"Unexpected error while updating marketplace: {str(e)}")
                raise HTTPException(status_code=500, detail="Failed to update marketplace") 

    async def delete(self, marketplace_id: str):
        try:
            if not ObjectId.is_valid(marketplace_id):
                raise HTTPException(status_code=400, detail="Invalid ID format")

            result = await self.collection.delete_one({"_id": ObjectId(marketplace_id)})

            if result.deleted_count == 0:
                raise HTTPException(status_code=404, detail="Marketplace not found")

            return {"deleted": True}

        except HTTPException:
            raise
        except Exception:
            logger.exception("Unexpected error while deleting marketplace")
            raise HTTPException(status_code=500, detail="Failed to delete marketplace")
