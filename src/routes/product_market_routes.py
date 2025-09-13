from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import MongoDBMotor
from schemas.responses import ResponseModel
from services.product_market_service import ProductMarketService
from schemas.product_market import ProductMarketUpdateSchema, ProductMarketCreateSchema, ProductMarketFilterSchema

router = APIRouter(prefix="/product_market", tags=["ProductMarket"])

# Inyectamos el servicio con la DB
# def get_service():
#     return ProductMarketervice()

def get_service( db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database)):
    return ProductMarketService(db)

# -------------------------
# RUTAS CRUD con Beanie
# -------------------------
@router.post("/", response_model=ResponseModel)
async def create_test( data: ProductMarketUpdateSchema, service: ProductMarketService = Depends(get_service)):
    test_id = await service.save(data)
    return ResponseModel(
        success=True,
        message="Test creado correctamente",
        data={"id": test_id},
        errors=None
    )

@router.get("/filter")
async def filter_test(
    filters: ProductMarketFilterSchema = Depends(),
    service: ProductMarketCreateSchema = Depends(get_service)
):
    result = await service.raw_find(filters)
    return ResponseModel(
        success=True,
        message="ProductMarket filtrados correctamente",
        data= result,
        errors=None
    )


@router.get("/{test_id}", response_model=ResponseModel)
async def get_test(test_id: str, service: ProductMarketService = Depends(get_service)):
    entity = await service.get_by_id(test_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    
    return ResponseModel(
        success=True,
        message="Test obtenido correctamente",
        data= entity,
        errors=None
    )


@router.get("/", response_model=ResponseModel)
async def get_all_test( service: ProductMarketService = Depends(get_service)):
    entity = await service.get_all()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    return ResponseModel(
        success=True,
        message="ProductMarket obtenidos correctamente",
        data= entity,
        errors=None
    )

@router.delete("/{test_id}", response_model=ResponseModel)
async def delete_test(
    test_id: str,
    service: ProductMarketService = Depends(get_service)
):

    entity = await service.delete(test_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    return ResponseModel(
        success=True,
        message="ProductMarket eliminados correctamente",
        data= entity,
        errors=None
    )

@router.put("/{test_id}", response_model=ResponseModel)
async def update_test(
    test_id: str,
    test: ProductMarketFilterSchema,
    service: ProductMarketService = Depends(get_service)
):
    result = await service.update(test_id, test )

    return ResponseModel(
        success=True,
        message="ProductMarket Actulizados correctamente",
        data= result,
        errors=None
    )
