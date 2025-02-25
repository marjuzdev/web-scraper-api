from database.config import stores_collection
from src.database.models import Store

def create_store(name, website):
    store = {"name": name, "website": website, "created_at": 0}
    stores_collection.insert_one(store)
    return {"message": "Tienda creada"}