from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, APIRouter
from routes.product_routes import router as product_routes
from routes.marketplace_routes import router as marketplace_routes
import logging
import sys

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    stream=sys.stdout  # 👈 Asegura que los logs vayan a la consola
)

logger = logging.getLogger(__name__)

app = FastAPI(title="Web Scrapper API")
api_router = APIRouter(prefix="/api")

api_router.include_router(product_routes)
api_router.include_router(marketplace_routes)
app.include_router(api_router)

@app.get("/")
async def root():
    logger.info("Web Scraper API working")
    return {"message": "Web Scraper API working"}