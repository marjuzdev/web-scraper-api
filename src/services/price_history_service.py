from bson import ObjectId
from repositories.price_history_repository import PriceHistoryRepository
from schemas.price_history import (
    PriceHistoryCreateSchema,
    PriceHistoryFilterSchema,
    PriceHistoryUpdateSchema,
)
from motor.motor_asyncio import AsyncIOMotorDatabase
from services.product_service import ProductService
from services.marketplace_service import MarketplaceService
from services.product_market_service import ProductMarketService


from playwright.async_api import async_playwright


class PriceHistoryService:

    def __init__(
        self,
        db: AsyncIOMotorDatabase,
        product_service: ProductService,
        marketplace_service: MarketplaceService,
        product_market_service: ProductMarketService
    ):
        self.db = db
        self.repository = PriceHistoryRepository(db)
        self.product_service = product_service
        self.marketplace_service = marketplace_service
        self.product_market_service = product_market_service
        

        async def get_prices():
            try:
                async with async_playwright() as p:
                    browser = await p.chromium.launch(headless=True)
                    page = await browser.new_page()

                    await page.goto("https://quotes.toscrape.com")
                    quotes = await page.query_selector_all(".quote")

                    data = []
                    for quote in quotes:
                        text = await (await quote.query_selector(".text")).inner_text()
                        author = await (await quote.query_selector(".author")).inner_text()
                        data.append({"text": text, "author": author})

                    await browser.close()
                    return data

            except Exception as e:
                return {"error": str(e)}
    

    async def get_prices_by_market(self, marketplace_id: str):
        return await self.product_market_service.get_products_by_marketplace_agg(marketplace_id)
 
    async def delete(self, test_id: str):
        return await self.repository.delete(test_id)

    async def update(self, test_id: str, test: PriceHistoryUpdateSchema):
        test_dict = test.model_dump(exclude_unset=True)
        return await self.repository.update(test_id, test_dict)

    async def raw_find(self, filters: PriceHistoryFilterSchema):
        filters = filters.model_dump(exclude_unset=True)

        limit = filters["limit"]
        return await self.repository.raw_find(filters, limit)
