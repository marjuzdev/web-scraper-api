from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import MongoDBMotor
from services.test_service import TestService
from schemas.test import TestSchema

router = APIRouter(prefix="/tests", tags=["Tests"])

# Inyectamos el servicio con la DB
def get_service():
    return TestService()

# -------------------------
# RUTAS CRUD con Beanie
# -------------------------
@router.post("/", response_model=dict)
async def create_test(test: TestSchema, service: TestService = Depends(get_service)):
    test_id = await service.save(test)
    return {"id": test_id}


@router.get("/{test_id}")
async def get_test(test_id: str, service: TestService = Depends(get_service)):
    entity = await service.get_by_id(test_id)
    if not entity:
        raise HTTPException(status_code=404, detail="Entity not found")
    return entity


# -------------------------
# RUTAS con consultas raw (Motor)
# -------------------------
@router.get("/country/{country}")
async def find_by_country(country: str, service: TestService = Depends(get_service)):
    return await service.find_by_country(country)


@router.get("/aggregate/countries")
async def aggregate_by_country(service: TestService = Depends(get_service)):
    return await service.aggregate_by_country()
