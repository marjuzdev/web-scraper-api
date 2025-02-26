from pydantic import BaseModel, Field
from typing import Optional
from database.models import PyObjectId
from bson import ObjectId

# Modelo de Producto
class Product(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")  # Manejo de ObjectId
    name: str
    description: Optional[str] = None
    # price: float
    store_id: Optional[str] = None  # ❌ CORREGIDO: Se usa Optional[str] en lugar de str?

    class Config:
        json_encoders = {ObjectId: str}  # Convierte ObjectId a JSON
        allow_population_by_field_name = True  # Permite usar `_id` en la entrada