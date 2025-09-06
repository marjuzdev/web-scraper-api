from typing import List
from fastapi import APIRouter, Depends
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import MongoDBMotor
from fastapi import APIRouter
from schemas.marketplace import MarketplaceSchema, MarketplaceUpdateSchema
from services.marketplace_service import  MarketplaceService

router = APIRouter(prefix="/marketplace", tags=["marketplace"])

@router.get("/", response_model=List[MarketplaceSchema])
async def get_marketplaces(
      db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database)
):
    service = MarketplaceService(db)
    result = await service.get_all()
    return result

@router.post("/")
async def create_marketplace(
    marketplace: MarketplaceSchema, 
    db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database)                
 ):
    service = MarketplaceService(db)
    result = await service.save(marketplace)
    return {"message": "Marketplace correctly registered", "marketplace": result}

@router.delete("/{marketplace_id}")
async def delete_marketplace(
    marketplace_id: str,
    db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database)
):
    service = MarketplaceService(db)
    await service.delete(marketplace_id)
    return {"message": "Marketplace deleted successfully"}

@router.put("/{marketplace_id}")
async def update_marketplace(
    marketplace_id: str,
    marketplace: MarketplaceUpdateSchema,
    db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database)
):
    service = MarketplaceService(db)
    result = await service.update(marketplace_id, marketplace )
    return {
        "message": "Marketplace updated successfully",
        "marketplace": result
    }