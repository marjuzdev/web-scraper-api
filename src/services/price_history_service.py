from bson import ObjectId
from common.utils.price_utils import parse_price
from logger import configure_logger
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

logger = configure_logger()

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


    async def get_prices_by_market(self, data: SyncPricesByMarketSchema):
        
        logger.info('initialize get_prices_by_market')

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

        print('products by marketplace mapping', results)
        prices_by_market = await self.scrape_all(products)
        print('scrapper - products by marketplace mapping', prices_by_market)

        for item in prices_by_market:
            item["price_discount"] = parse_price(item.get("price_discount"))

        print('scrapper normalize prices - products by marketplace mapping', prices_by_market)

        data_map = [
            {
                "product_market_id": item["product_market_id"],
                "price_discount": item["price_discount"],
            }
            for item in prices_by_market
        ]

        print('scrapper normalize prices - data_map', prices_by_market)
        await self.repository.save_batch(data_map)
        return True


    async def scrape_all(self, products: list[dict]):
        results = []

        async with async_playwright() as p:
            print("🟢 Playwright iniciado")
            browser = await p.chromium.launch(
                headless=True,
                args=["--no-sandbox", "--disable-setuid-sandbox", "--disable-dev-shm-usage",
                    "--disable-gpu", "--disable-software-rasterizer"]
            )
            print("🌐 Navegador Chromium lanzado")

            context = await browser.new_context(
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/140.0.0.0 Safari/537.36"
                )
            )
            print("📂 Contexto de navegador creado con User-Agent")

            page = await context.new_page()
            print("📄 Nueva pestaña abierta")

            for product in products:
                url = product.get("url")
                selectors = product.get("selectors", {})
                product_id = product.get("product_market_id")
                data = {"url": url, "product_market_id": product_id}

                print(f"🚀 Iniciando scraping de: {url}")
                try:
                    await page.goto(url, wait_until="domcontentloaded", timeout=60000)
                    print(f"✅ Página cargada correctamente: {url}")

                    await page.wait_for_timeout(2000)  # espera extra si la página usa Render

                    for key, selector in selectors.items():
                        if not selector:
                            data[key] = None
                            continue

                        print(f"🔍 Buscando selector '{key}': {selector}")
                        try:
                            await page.wait_for_selector(selector, timeout=15000)
                            el = await page.query_selector(selector)
                            data[key] = await el.inner_text() if el else None
                            print(f"🎯 Valor encontrado para '{key}': {data[key]}")
                        except Exception:
                            data[key] = None
                            print(f"⚠️ No se pudo obtener '{key}' para {url}")

                except Exception as e:
                    data["error"] = str(e)
                    print(f"🔥 Error durante scraping de {url}: {e}")

                results.append(data)

            await browser.close()
            print("🛑 Navegador cerrado")

        print("🏁 Proceso finalizado, resultados listos")
        return results


    async def delete(self, test_id: str):
        return await self.repository.delete(test_id)

    async def update(self, test_id: str, test: PriceHistoryUpdateSchema):
        test_dict = test.model_dump(exclude_unset=True)
        return await self.repository.update(test_id, test_dict)

    async def raw_find(self, filters: PriceHistoryFilterSchema):
        filters = filters.model_dump(exclude_unset=True)

        limit = filters["limit"]
        return await self.repository.raw_find(filters, limit)
