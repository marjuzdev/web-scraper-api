from typing import Optional
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from entities.product_entity import ProductEntity
from entities.marketplace_entity import MarketplaceEntity
from entities.product_market_entity import ProductMarketEntity
from entities.price_history_entity import PriceHistoryEntity
from entities.test_entity import TestEntity

from seed.constants.products import products_data
from seed.constants.marketplaces import marketplaces_data
from seed.constants.product_market import product_market_data
from seed.constants.price_history import price_history_data
from logger import configure_logger

logger = configure_logger()

class SeedService:
    def __init__(self, db: Optional[AsyncIOMotorDatabase] = None):
        self.db = db

    async def execute_seed(self):
        logger.info("Ejecutando seed...")

        await TestEntity.delete_all()
        await ProductEntity.delete_all()
        await MarketplaceEntity.delete_all()
        await ProductMarketEntity.delete_all()
        await PriceHistoryEntity.delete_all()

        # # Insertar marketplaces
        marketplaces = [MarketplaceEntity(**data) for data in marketplaces_data]
        await MarketplaceEntity.insert_many(marketplaces)
        logger.info(f"Inserted {len(marketplaces)} marketplaces")
        # # Insertar productos
        products = [ProductEntity(**data) for data in products_data]
        await ProductEntity.insert_many(products)
        logger.info(f"Inserted {len(products)} products")

        # Insertar product_market
        product_markets = []
        for pm in product_market_data:
            product = await ProductEntity.find_one(ProductEntity.name == pm["product_name"])
            marketplace = await MarketplaceEntity.find_one(MarketplaceEntity.name == pm["marketplace_name"])

            if product and marketplace:
                product_markets.append(
                    ProductMarketEntity(
                        product_id=product.id,
                        marketplace_id=marketplace.id,
                        url=pm["url"],
                        available=pm["available"],
                    )
                )

        await ProductMarketEntity.insert_many(product_markets)
        logger.info(f"Inserted {len(product_markets)} product_market entries")

        return {"message": "Seed ejecutado correctamente"}
