from dotenv import load_dotenv
load_dotenv()

from routes.product_routes import router as product_routes
from fastapi import FastAPI

app = FastAPI(title="Web Scrapper API")

app.include_router(product_routes, prefix="/api")

@app.get("/")
async def root():
    return {"message": "API de Web Scraper funcionando"}