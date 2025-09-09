import os
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

class MongoDBMotor:
    """Singleton para conexión cruda con Motor."""
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
            self.db = self.client[self.database_name]

            print("✅ Conectado a MongoDB con Motor")

    def get_db(self) -> AsyncIOMotorDatabase:
        return self.db
    
    # Factory Method para inyección de dependencias
    @classmethod
    async def get_database(cls) -> AsyncIOMotorDatabase:
        mongo = cls()
        await mongo.init_connection()
        return mongo.get_db()