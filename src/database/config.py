import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

class MongoDB:
    """Clase Singleton para gestionar la conexión a MongoDB."""
    _instance = None  # Variable para la instancia única

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    async def init_connection(self):
        """Inicializa la conexión con MongoDB de forma asíncrona."""
        if not hasattr(self, "client"):  # Evita reinicialización
            self.username = os.getenv("MONGO_USERNAME")
            self.password = os.getenv("MONGO_PASSWORD")
            self.host = os.getenv("MONGO_HOST")
            self.database_name = os.getenv("MONGO_DATABASE")
            self.options = os.getenv("MONGO_OPTIONS")

            uri = f"mongodb+srv://{self.username}:{self.password}@{self.host}/{self.database_name}{self.options}"
            self.client = AsyncIOMotorClient(uri)
            self.db = self.client[self.database_name]

            print("✅ Conectado a MongoDB")

    def get_db(self) -> AsyncIOMotorDatabase:
        """Retorna la instancia de la base de datos."""
        return self.db

# Factory Method para inyección de dependencias
async def get_database() -> AsyncIOMotorDatabase:
    mongo = MongoDB()
    await mongo.init_connection()
    return mongo.get_db()
