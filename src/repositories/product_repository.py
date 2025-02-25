from motor.motor_asyncio import AsyncIOMotorDatabase
from schemas.product import ProductSchema


class ProductRepository:
    """Repositorio para gestionar los productos en MongoDB."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["products"]

    async def save(self, product: dict):
        result = await self.collection.insert_one(product)
        return str(result.inserted_id)

