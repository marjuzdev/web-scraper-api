from fastapi import APIRouter, Depends, HTTPException
from database.config import get_database
from repositories.product_repository import ProductRepository
from schemas.product import ProductModel, ProductSchema
from services.product_service import ProductService
from motor.motor_asyncio import AsyncIOMotorDatabase


router = APIRouter(prefix="/products", tags=["Products"])


@router.post("/")
async def create_product(
    product: ProductSchema,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    repository = ProductRepository(db)
    service = ProductService(repository)
    result = await service.create_product(product)
    return {"message": "Producto registrado con éxito", "product": result}

# Obtener una producto por ID
@router.get("/{product_id}")
async def get_product(
    product_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    try:
        repository = ProductRepository(db)
        service = ProductService(repository)
        product = await service.get_product(product_id)
        return product
    
    except Exception as error: 
        print('Ha occurido un problema', error)
        raise HTTPException(status_code=400, detail=f"Error: {str(error)}")
 

