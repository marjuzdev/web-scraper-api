from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import MongoDBMotor
from schemas.responses import ResponseModel
from .seed_service import SeedService

router = APIRouter(prefix="/seed", tags=["seed"])

def get_service( db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database)):
    return SeedService(db)

@router.get("/", response_model=ResponseModel)
async def execute_seed( service: SeedService = Depends(get_service)):

    response = await service.execute_seed()
    return ResponseModel(
        success=True,
        message="Seed creado correctamente",
        data= response,
        errors=None
    )
