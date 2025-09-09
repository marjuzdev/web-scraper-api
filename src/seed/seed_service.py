# from ..entities.product_entity import

from typing import Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from .constants.marketplaces import marketplaces_data
from .constants.products import products_data
from entities.test_entity import TestEntity
from logger import configure_logger

logger = configure_logger()

class SeedService:

    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None ):
        self.db = db

    async def execute_seed(self):

        docs = await self.db['marketplaces'].find().to_list(length=100)
        return [
            {**doc, "_id": str(doc["_id"])} 
            if "_id" in doc and isinstance(doc["_id"], ObjectId) else doc
            for doc in docs
        ]


        # docs = await self.db.collection['test'].find().to_list(length=100)
        # return [
        #     {**doc, "_id": str(doc["_id"])} 
        #     if "_id" in doc and isinstance(doc["_id"], ObjectId) else doc
        #     for doc in docs
        # ]


