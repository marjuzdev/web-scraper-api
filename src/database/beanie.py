import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from beanie import init_beanie
from entities import all_entities 


class MongoDBBeanie:
    """Singleton para conexión con Beanie."""
    _instance = None  

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def init_connection(self):
        if not hasattr(self, "client"):
            self.username = os.getenv("MONGO_USERNAME")
            self.password = os.getenv("MONGO_PASSWORD")
            self.host = os.getenv("MONGO_HOST")
            self.database_name = os.getenv("MONGO_DATABASE")
            self.options = os.getenv("MONGO_OPTIONS", "")

            uri = f"mongodb+srv://{self.username}:{self.password}@{self.host}/{self.database_name}{self.options}"
            self.client = AsyncIOMotorClient(uri)
            self.db: AsyncIOMotorDatabase = self.client[self.database_name]

            if all_entities:
                await init_beanie(database=self.db, document_models=all_entities)
                print(f"✅ Conectado a MongoDB con Beanie ({len(all_entities)} modelos)")
            else:
                print("⚠️ No se registraron modelos en Beanie (lista vacía)")

    async def close(self):
        """Cierra la conexión con MongoDB."""
        if hasattr(self, "client"):
            self.client.close()
            print("🔴 Conexión a MongoDB cerrada")

    def get_db(self) -> AsyncIOMotorDatabase:
        return self.db
