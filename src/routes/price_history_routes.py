from fastapi import APIRouter, Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from database import MongoDBMotor
from schemas.responses import ResponseModel
from services.price_history_service import PriceHistoryService
from schemas.price_history import (
    SyncPricesByMarketSchema
)
from services.product_market_service import ProductMarketService
from services.product_service import ProductService
from services.marketplace_service import MarketplaceService


router = APIRouter(prefix="/price_history", tags=["PriceHistory"])

def get_product_market_service(
    db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database),
):
    return ProductMarketService(db)


def get_product_service(
    db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database),
):
    return ProductService(db)


def get_marketplace_service(
    db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database),
):
    return MarketplaceService(db)


def get_price_history_service(
    db: AsyncIOMotorDatabase = Depends(MongoDBMotor.get_database),
    product_service: ProductService = Depends(get_product_service),
    marketplace_service: MarketplaceService = Depends(get_marketplace_service),
    product_market_service: ProductMarketService = Depends(get_product_market_service),
):
    return PriceHistoryService(
        db,
        product_service,
        marketplace_service,
        product_market_service,
    )

@router.post("/", response_model=ResponseModel)
async def sync_prices_by_market(
    data: SyncPricesByMarketSchema,
    priceHistoryService: PriceHistoryService = Depends(get_price_history_service),
):  
    response = await priceHistoryService.get_prices_by_market(data)

    return ResponseModel(
        success=True,
        message="Precios sincronizados correctamente",
        data=response,
        errors=None,
    )
