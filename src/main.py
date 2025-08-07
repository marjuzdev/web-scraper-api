from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, APIRouter
from routes.product_routes import router as product_routes
from routes.marketplace_routes import router as marketplace_routes
from playwright.async_api import async_playwright
from logger import configure_logger

logger = configure_logger()

app = FastAPI(title="Web Scrapper API")
api_router = APIRouter(prefix="/api")

api_router.include_router(product_routes)
api_router.include_router(marketplace_routes)
app.include_router(api_router)

@app.get("/")
async def root():
    logger.info("Web Scraper API working")
    return {"message": "Web Scraper API working"}


@app.get("/quotes")
async def get_quotes():
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