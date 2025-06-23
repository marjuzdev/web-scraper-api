import os 
os.environ["PLAYWRIGHT_BROWSERS_PATH"] = "0"

from fastapi import APIRouter, Depends, HTTPException
from playwright.async_api import async_playwright
from motor.motor_asyncio import AsyncIOMotorDatabase

from schemas.product import ProductModel, ProductSchema
from services.product_service import ProductService
from repositories.product_repository import ProductRepository
from database.config import get_database


router = APIRouter(prefix="/products", tags=["Products"])

@router.get("/quotes")
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
    
# Obtener una producto por ID
@router.get("/{product_id}")
async def get_product(
    product_id: str,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    try:
        repository = ProductRepository(db)
        service = ProductService(repository)
        product = await service.get_product(product_id)
        return product
    
    except Exception as error: 
        print('Ha occurido un problema', error)
        raise HTTPException(status_code=400, detail=f"Error: {str(error)}")
    

@router.post("/")
async def create_product(
    product: ProductSchema,
    db: AsyncIOMotorDatabase = Depends(get_database)
):
    repository = ProductRepository(db)
    service = ProductService(repository)
    result = await service.create_product(product)
    return {"message": "Producto registrado con éxito", "product": result}




 

