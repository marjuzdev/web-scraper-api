from bson import ObjectId
from common.utils.price_utils import parse_price
from repositories.price_history_repository import PriceHistoryRepository
from schemas.price_history import (
    PriceHistoryCreateSchema,
    PriceHistoryFilterSchema,
    PriceHistoryUpdateSchema,
    SyncPricesByMarketSchema,
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

    async def scrape_all(self, products: list[dict]):
        results = []

        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()

            for product in products:
                url = product["url"]
                selectors = product["selectors"]
                product_id = product.get("product_market_id")

                data = {"url": url, "product_market_id": product_id}
                try:
                    await page.goto(url)

                    # Recorremos dinámicamente los selectores
                    for key, selector in selectors.items():
                        if not selector:
                            data[key] = None
                            continue
                        el = await page.query_selector(selector)
                        data[key] = await el.inner_text() if el else None

                except Exception as e:
                    data["error"] = str(e)

                results.append(data)

            await browser.close()

        return results

    async def get_prices_by_market(self, data: SyncPricesByMarketSchema):

        results = await self.product_market_service.get_products_by_marketplace_agg(
            data.marketplace_id
        )

        products = [
            {
                "url": item["product_url"],
                "selectors": item["marketplace_css_selectors"],
                "product_market_id": item["_id"],
            }
            for item in results
        ]

        prices_by_market = await self.scrape_all(products)

        for item in prices_by_market:
            item["price_discount"] = parse_price(item["price_discount"])

        data_map = [
            {
                "product_market_id": item["product_market_id"],
                "price_discount": item["price_discount"],
            }
            for item in prices_by_market
        ]
        await self.repository.save_batch(data_map)
        return True


    async def delete(self, test_id: str):
        return await self.repository.delete(test_id)

    async def update(self, test_id: str, test: PriceHistoryUpdateSchema):
        test_dict = test.model_dump(exclude_unset=True)
        return await self.repository.update(test_id, test_dict)

    async def raw_find(self, filters: PriceHistoryFilterSchema):
        filters = filters.model_dump(exclude_unset=True)

        limit = filters["limit"]
        return await self.repository.raw_find(filters, limit)
