from typing import Union
from fastapi import FastAPI

from dotenv import load_dotenv
load_dotenv()

from pymongo import MongoClient
from mongo_config import MongoDBConfig
from pymongo.server_api import ServerApi

app = FastAPI(
    title="Web Scrapper API"
)
# Obtener la URI de conexión
MONGO_URI = MongoDBConfig.get_connection_uri()
client = MongoClient(MONGO_URI, server_api=ServerApi('1'))
    
@app.get("/")
def read_root():
    try:
        client.admin.command("ping")
        print("✅ Conexión exitosa a MongoDB Atlas")
        return {"message": "Conexión exitosa a MongoDB Atlas"}
    except Exception as e:
        print(f"❌ Error de conexión: {e}")
        return {"message": "Error de conexión"}
 

@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}



