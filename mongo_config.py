
import os

class MongoDBConfig:
    """Clase para gestionar la configuración de MongoDB."""
    USERNAME = os.getenv("MONGO_USERNAME")
    PASSWORD = os.getenv("MONGO_PASSWORD")
    HOST = os.getenv("MONGO_HOST")
    DATABASE = os.getenv("MONGO_DATABASE")
    OPTIONS = os.getenv("MONGO_OPTIONS")

    @classmethod
    def get_connection_uri(cls):
        """Genera la URI de conexión de forma segura."""
        return f"mongodb+srv://{cls.USERNAME}:{cls.PASSWORD}@{cls.HOST}/{cls.DATABASE}{cls.OPTIONS}"