from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId

class ProductRepository:

    def __init__(self, db: AsyncIOMotorDatabase):
        self.collection = db["products"]

    async def save(self, product: dict):
        result = await self.collection.insert_one(product)
        return str(result.inserted_id)
    
    async def get_product(self, product_id: str):

        try:
            product = await self.collection.find_one({"_id": ObjectId(product_id)})
            if not product:
                raise HTTPException(status_code=404, detail="Producto no encontrado")
            
            product["id"] = str(product.pop("_id"))
            return product
        
        except Exception as error:
            print(f"Error: {error}")
            raise error



