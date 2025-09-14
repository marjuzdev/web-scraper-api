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

    async def scrape_all(self, products):
        results = []
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()  # Usamos **una sola pestaña**
            
            for product in products:
                url = product["url"]
                selectors = product["selectors"]
                try:
                    await page.goto(url)
                    data = {"url": url}

                    if selectors.get("price_normal"):
                        el = await page.query_selector(selectors["price_normal"])
                        data["price_normal"] = await el.inner_text() if el else None

                    if selectors.get("price_discount"):
                        el = await page.query_selector(selectors["price_discount"])
                        data["price_discount"] = await el.inner_text() if el else None

                    results.append(data)

                except Exception as e:
                    results.append({"url": url, "error": str(e)})

            await browser.close()
        return results

    async def get_prices_by_market(self, marketplace_id: str):
        results = await self.product_market_service.get_products_by_marketplace_agg(
            marketplace_id
        )

        products = list(map(lambda data: {'url': data['product_url'], 'selectors': data['marketplace_css_selectors']}, results))
        result= await self.scrape_all(products)
        return result

    async def delete(self, test_id: str):
        return await self.repository.delete(test_id)

    async def update(self, test_id: str, test: PriceHistoryUpdateSchema):
        test_dict = test.model_dump(exclude_unset=True)
        return await self.repository.update(test_id, test_dict)

    async def raw_find(self, filters: PriceHistoryFilterSchema):
        filters = filters.model_dump(exclude_unset=True)

        limit = filters["limit"]
        return await self.repository.raw_find(filters, limit)
