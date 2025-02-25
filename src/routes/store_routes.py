from fastapi import APIRouter

router = APIRouter()

class StoreRoutes:
    @router.get("/stores")
    async def get_stores():
        return {"message": "Lista de tiendas"}

    @router.post("/stores")
    async def create_store(store: dict):
        return {"message": "Tienda creada", "store": store}

    @router.get("/stores/{store_id}")
    async def get_store(store_id: str):
        return {"message": f"Detalles de la tienda {store_id}"}
