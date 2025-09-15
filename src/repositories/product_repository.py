from fastapi import HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from bson import ObjectId, errors
from logger import configure_logger

logger = configure_logger()

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
            if isinstance(error, errors.InvalidId):
                raise HTTPException(status_code=400, detail="ID inválido")
            if isinstance(error, HTTPException):
                raise error
            raise HTTPException(status_code=500, detail="Error al buscar el producto")
        
    
    async def get_all(self):
        try:
            
            docs = await self.collection.find().to_list()
            return [
                {**doc, "_id": str(doc["_id"])} 
                if "_id" in doc and isinstance(doc["_id"], ObjectId) else doc
                for doc in docs
            ]
        
        except Exception:
            logger.exception("Unexpected error while listing products")
            raise HTTPException(status_code=500, detail="Failed to list products")
    


