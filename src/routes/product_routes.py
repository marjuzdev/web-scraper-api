from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase

from schemas.product import ProductSchema
from services.product_service import ProductService
from database import MongoDBMotor

router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/{product_id}")
async def get_product(
    product_id: str,
    db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database)
):
    try:
        service = ProductService(db)
        product = await service.get_product(product_id)
        return product
    
    except Exception as error: 
        print('Ha occurido un problema', error)
        raise HTTPException(status_code=400, detail=f"Error: {str(error)}")
    
@router.post("/")
async def create_product(
    product: ProductSchema,
    db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database)
):
    service = ProductService(db)
    result = await service.create_product(product)
    return {"message": "Producto registrado con éxito", "product": result}




 

