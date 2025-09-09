from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import MongoDBMotor
from schemas.responses import ResponseModel
from services.test_service import TestService
from schemas.test import TestCreateSchema, TestFilterSchema, TestUpdateSchema

router = APIRouter(prefix="/tests", tags=["Tests"])

# Inyectamos el servicio con la DB
# def get_service():
#     return TestService()

def get_service( db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database)):
    return TestService(db)

# -------------------------
# RUTAS CRUD con Beanie
# -------------------------
@router.post("/", response_model=ResponseModel)
async def create_test(test: TestCreateSchema, service: TestService = Depends(get_service)):
    test_id = await service.save(test)
    return ResponseModel(
        success=True,
        message="Test creado correctamente",
        data={"id": test_id},
        errors=None
    )

@router.get("/filter")
async def filter_test(
    filters: TestFilterSchema = Depends(),
    service: TestService = Depends(get_service)
):
    result = await service.raw_find(filters)
    return ResponseModel(
        success=True,
        message="Tests filtrados correctamente",
        data= result,
        errors=None
    )


@router.get("/{test_id}", response_model=ResponseModel)
async def get_test(test_id: str, service: TestService = Depends(get_service)):
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
async def get_all_test( service: TestService = Depends(get_service)):
    entity = await service.get_all()
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")

    return ResponseModel(
        success=True,
        message="Tests obtenidos correctamente",
        data= entity,
        errors=None
    )

@router.delete("/{test_id}", response_model=ResponseModel)
async def delete_test(
    test_id: str,
    service: TestService = Depends(get_service)
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
    test: TestUpdateSchema,
    service: TestService = Depends(get_service)
):
    result = await service.update(test_id, test )

    return ResponseModel(
        success=True,
        message="Tests Actulizados correctamente",
        data= result,
        errors=None
    )



@router.get("/aggregate/countries")
async def aggregate_by_country(service: TestService = Depends(get_service)):
    return await service.aggregate_by_country()
