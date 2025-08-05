from dotenv import load_dotenv
load_dotenv()

from fastapi import FastAPI, APIRouter
from routes.product_routes import router as product_routes
from routes.marketplace_routes import router as marketplace_routes

app = FastAPI(title="Web Scrapper API")
api_router = APIRouter(prefix="/api")

api_router.include_router(product_routes)
api_router.include_router(marketplace_routes)
app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "API de Web Scraper funcionando"}