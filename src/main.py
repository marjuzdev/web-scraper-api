from fastapi import FastAPI
from dotenv import load_dotenv
load_dotenv()

from routes.product_routes import router as product_routes

app = FastAPI(title="Web Scrapper API")

app.include_router(product_routes, prefix="/api")
@app.get("/")
async def root():
    return {"message": "API de Web Scraper funcionando"}

# from database.config import get_database
# import asyncio

# async def main():
#     await get_database()
    
# asyncio.run(main())

