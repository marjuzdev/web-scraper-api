from fastapi import HTTPException
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from logger import configure_logger
from entities.test_entity import TestEntity

logger = configure_logger()

class TestRepository:
    
    def __init__(self, db: AsyncIOMotorDatabase = None):
        self.collection = db["marketplaces"] if db else None

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

    # -----------------------------
    # Funciones opcionales con Motor
    # -----------------------------
    async def raw_find(self, filter_query: dict, limit: int = 50):
        if not self.collection:
            raise HTTPException(status_code=500, detail="Motor not initialized")
        try:
            return await self.collection.find(filter_query).to_list(length=limit)
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
