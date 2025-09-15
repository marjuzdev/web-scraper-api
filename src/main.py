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

@app.get("/")
async def root():
    logger.info("Web Scraper API working")
    return {"message": "Web Scraper API working"}