from typing import List
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException
from fastapi.encoders import jsonable_encoder
from motor.motor_asyncio import AsyncIOMotorDatabase
from database.config import get_database
from fastapi import APIRouter
from schemas.marketplace import MarketplaceSchema
from services.marketplace_service import  MarketplaceService

router = APIRouter(prefix="/marketplace", tags=["marketplace"])

@router.get("/", response_model=List[MarketplaceSchema])
async def get_marketplaces(
      db: AsyncIOMotorDatabase = Depends(get_database)
):
    service = MarketplaceService(db)
    result = await service.get_all()
    return result

@router.post("/")
async def create_marketplace(
    marketplace: MarketplaceSchema, 
    db: AsyncIOMotorDatabase = Depends(get_database)                
 ):
    service = MarketplaceService(db)
    result = await service.save(marketplace)
    return {"message": "Tienda registrada correctamente", "marketplace": result}


