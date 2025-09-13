from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import MongoDBMotor
from schemas.responses import ResponseModel
from services.price_history_service import PriceHistoryService
from schemas.price_history import PriceHistoryCreateSchema, PriceHistoryFilterSchema, PriceHistoryUpdateSchema

router = APIRouter(prefix="/price_history", tags=["PriceHistory"])

def get_service( db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database)):
    return PriceHistoryService(db)


@router.post("/", response_model=ResponseModel)
async def create_test( data: PriceHistoryCreateSchema, service: PriceHistoryService = Depends(get_service)):
    test_id = await service.save(data)
    return ResponseModel(
        success=True,
        message="Price creado correctamente",
        data={"id": test_id},
        errors=None
    )

@router.get("/filter")
async def filter_test(
    filters: PriceHistoryFilterSchema = Depends(),
    service: PriceHistoryService = Depends(get_service)
):
    result = await service.raw_find(filters)
    return ResponseModel(
        success=True,
        message="Tests filtrados correctamente",
        data= result,
        errors=None
    )


@router.get("/{test_id}", response_model=ResponseModel)
async def get_test(test_id: str, service: PriceHistoryService = Depends(get_service)):
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
async def get_all_test( service: PriceHistoryService = Depends(get_service)):
    # entity = await service.get_all()
    # if not entity:
    #     raise HTTPException(status_code=404, detail="Entity not found")

    return ResponseModel(
        success=True,
        message="Prices obtenidos correctamente",
        data= 'entity',
        errors=None
    )

@router.delete("/{test_id}", response_model=ResponseModel)
async def delete_test(
    test_id: str,
    service: PriceHistoryService = Depends(get_service)
):

    entity = await service.delete(test_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    return ResponseModel(
        success=True,
        message="Tests eliminados correctamente",
        data= entity,
        errors=None
    )

@router.put("/{test_id}", response_model=ResponseModel)
async def update_test(
    test_id: str,
    test: PriceHistoryUpdateSchema,
    service: PriceHistoryService = Depends(get_service)
):
    result = await service.update(test_id, test )

    return ResponseModel(
        success=True,
        message="Tests Actulizados correctamente",
        data= result,
        errors=None
    )