from beanie import PydanticObjectId
from fastapi import HTTPException
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from logger import configure_logger
from entities.test_entity import TestEntity

logger = configure_logger()

class TestRepository:
    
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.collection = db["test"] if db is not None else None

    # -----------------------------
    # CRUD con Beanie
    # -----------------------------
    async def save(self, entity: dict):
        try:
            existing = await TestEntity.find_one(TestEntity.name == entity.get("name"))
            if existing:
                raise HTTPException(status_code=400, detail="Entity name already exists")

            new_entity = TestEntity(**entity)
            await new_entity.insert()
            return str(new_entity.id)
        except HTTPException:
            raise
        except Exception as e:
            logger.exception(f"Error saving entity: {e}")
            raise HTTPException(status_code=500, detail="Failed to create entity")

    async def get_by_id(self, entity_id: str):
        if not ObjectId.is_valid(entity_id):
            raise HTTPException(status_code=400, detail="Invalid ID format")

        entity = await TestEntity.get(ObjectId(entity_id))
        if not entity:
            raise HTTPException(status_code=404, detail="Entity not found")
        return entity
    
    async def get_all(self):
        try:

            docs = await TestEntity.find().to_list(100)
            return [
                {**doc, "_id": str(doc["_id"])} 
                if "_id" in doc and isinstance(doc["_id"], ObjectId) else doc
                for doc in docs
            ]
        
        except Exception:
            logger.exception("Unexpected error while listing marketplaces")
            raise HTTPException(status_code=500, detail="Failed to list marketplaces")
        
    async def delete(self, test_id: str):
        try:
            if not PydanticObjectId.is_valid(test_id):
                raise HTTPException(status_code=400, detail="Invalid ID format")

            test = await TestEntity.get(PydanticObjectId(test_id))
            if not test:
                raise HTTPException(status_code=404, detail="Test not found")

            await test.delete()
            return {"deleted": True}
        except HTTPException:
            raise
        except Exception:
            logger.exception("Unexpected error while deleting test entity")
            raise HTTPException(status_code=500, detail="Failed to delete test entity")
        
    async def update(self, test_id: str, update_data: dict):
        try:
            if not PydanticObjectId.is_valid(test_id):
                raise HTTPException(status_code=400, detail="Invalid ID format")

            result = await TestEntity.find_one(
                TestEntity.id == PydanticObjectId(test_id)
            ).update({"$set": update_data})

            if result is None:
                raise HTTPException(status_code=404, detail="Test not found")

            return {"updated": True}

        except HTTPException as e:
            logger.error(f"HTTPException: {e.detail}")
            raise e
        except Exception as e:
            logger.exception(f"Unexpected error while updating test entity: {str(e)}")
            raise HTTPException(status_code=500, detail="Failed to update test entity")

    # -----------------------------
    # Funciones opcionales con Motor
    # -----------------------------
    async def raw_find(self, filter_query: dict, limit: int = 50):
        
        if self.collection is None:
            raise HTTPException(status_code=500, detail="Motor not initialized")
         
        try:
            filter_mongo = {}
            if filter_query.get("name") is not None:
                filter_mongo["name"] = {"$regex": filter_query["name"], "$options": "i"}

            if filter_query.get("country") is not None:
                filter_mongo["country"] = {"$eq": filter_query["country"]}

            docs = await self.collection.find(filter_mongo).to_list(length=limit)

            return [
                {**doc, "_id": str(doc["_id"])} 
                if "_id" in doc and isinstance(doc["_id"], ObjectId) else doc
                for doc in docs
            ]
        
        except Exception as e:
            logger.exception(f"Error in raw find: {e}")
            raise HTTPException(status_code=500, detail="Failed raw query")

    async def raw_aggregate(self, pipeline: list):
        if not self.collection:
            raise HTTPException(status_code=500, detail="Motor not initialized")
        try:
            cursor = self.collection.aggregate(pipeline)
            return [doc async for doc in cursor]
        except Exception as e:
            logger.exception(f"Error in aggregation: {e}")
            raise HTTPException(status_code=500, detail="Failed aggregation")
