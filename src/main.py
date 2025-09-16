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
    selector = ".vtex-product-price-1-x-sellingPrice .vtex-product-price-1-x-currencyContainer"

    data = {"url": url, "price_discount": None, "error": None}

    print("🚀 Iniciando scraping de:", url)

    async with async_playwright() as p:
        print("🟢 Playwright iniciado")

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
        print("🌐 Navegador Chromium lanzado")

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                       "AppleWebKit/537.36 (KHTML, like Gecko) "
                       "Chrome/140.0.0.0 Safari/537.36"
        )
        print("📂 Contexto de navegador creado con User-Agent")

        page = await context.new_page()
        print("📄 Nueva pestaña abierta")

        try:
            print("➡️ Navegando hacia:", url)
            await page.goto(url, wait_until="domcontentloaded")
            print("✅ Página cargada correctamente")

            # ⚡ Extra espera para Render (2s)
            await page.wait_for_timeout(2000)

            print(f"🔍 Buscando selector: {selector}")
            el = await page.query_selector(selector)

            if el:
                text_value = await el.inner_text()
                print(f"🎯 Selector encontrado → {text_value}")
                data["price_discount"] = text_value
            else:
                print(f"⚠️ Selector '{selector}' no encontrado en la página")
                data["price_discount"] = None

        except Exception as e:
            print(f"🔥 Error durante scraping: {e}")
            data["error"] = str(e)

        finally:
            await browser.close()
            print("🛑 Navegador cerrado")

    print("🏁 Proceso finalizado, data lista para devolver")
    return {"data": data}


