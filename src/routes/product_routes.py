from fastapi import APIRouter, Depends
from database.config import get_database
from repositories.product_repository import ProductRepository
from schemas.product import ProductSchema
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
