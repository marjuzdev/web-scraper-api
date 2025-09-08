

from dotenv import load_dotenv

from entities import TestEntity
from schemas.responses import ResponseModel
from schemas.test import TestSchema
load_dotenv()

from contextlib import asynccontextmanager

from database import MongoDBBeanie

from fastapi import FastAPI, APIRouter, HTTPException
from routes.product_routes import router as product_routes
from routes.marketplace_routes import router as marketplace_routes
from playwright.async_api import async_playwright
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
    

@app.get("/beanie")
async def beanie():
    try:
        test = TestEntity(name="Ejemplo", url_base="http://test.com", country="CO")
        await test.insert()
        return test.model_dump()
    except HTTPException:
            raise
    except Exception:
            logger.exception("Unexpected error while retrieving marketplace by ID")
            raise HTTPException(status_code=500, detail="Failed to retrieve t")
    


@app.post("/beanie", response_model=ResponseModel)
async def create_test(test_schema: TestSchema):
    try:
        data = test_schema.model_dump()
        data["url_base"] = str(data["url_base"])
        test = TestEntity(**data)
        await test.insert()

        response = ResponseModel(
            message="TestEntity creada exitosamente",
            data = test
        )
        return response
        
    except Exception:
        logger.exception("Unexpected error while creating TestEntity")
        raise HTTPException(status_code=500, detail="Failed to create entity")



