from dotenv import load_dotenv
load_dotenv()
from contextlib import asynccontextmanager
from database import MongoDBBeanie
from fastapi import FastAPI, APIRouter
from routes.product_routes import router as product_routes
from routes.marketplace_routes import router as marketplace_routes
from routes.product_market_routes import router as product_market_routes
from routes.price_history_routes import router as price_history_routes
from seed.seed_routes import router as seed_routes
from routes.test_routes import router as test_routes
from logger import configure_logger

logger = configure_logger()

@asynccontextmanager
async def lifespan(app: FastAPI):
    await MongoDBBeanie().init_connection()
    yield
    print("👋 Conexión a MongoDB cerrada")

app = FastAPI(title="Web Scrapper API", lifespan=lifespan)
api_router = APIRouter(prefix="/api")

api_router.include_router(product_routes)
api_router.include_router(marketplace_routes)
api_router.include_router(product_market_routes)
api_router.include_router(price_history_routes)
api_router.include_router(test_routes)
api_router.include_router(seed_routes)
app.include_router(api_router)

from playwright.async_api import async_playwright

@app.get("/")
async def root():
    logger.info("Web Scraper API working")
    return {"message": "Web Scraper API working"}


@app.get("/quotes")
async def quotes():
    url = "https://www.cutis.com.co/hiclina-100-mg-capsulas/p"
    selectors = {
        "price_discount": ".vtex-product-price-1-x-sellingPrice .vtex-product-price-1-x-currencyContainer",
        "price_normal": ".vtex-product-price-1-x-listPriceValue"
    }

    async with async_playwright() as p:
        browser = await p.chromium.launch(
            headless=True,
            args=[
                "--no-sandbox",
                "--disable-setuid-sandbox",
                "--disable-dev-shm-usage",
                "--disable-gpu",
                "--disable-software-rasterizer"
            ]
        )
        page = await (await browser.new_context()).new_page()
        await page.goto(url, wait_until="domcontentloaded")

        data = {"url": url}
        for key, selector in selectors.items():
            try:
                el = await page.wait_for_selector(selector, timeout=5000)
                data[key] = await el.inner_text() if el else None
            except:
                data[key] = None

        await browser.close()

    return {"data": data}