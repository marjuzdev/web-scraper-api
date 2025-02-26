from pydantic import BaseModel, Field
from datetime import datetime
from bson import ObjectId
from typing import Optional

from database.models import PyObjectId

# class ProductSchema(BaseModel):
#     name: str  # Campo obligatorio
#     description: Optional[str] = None  # Campo opcional


class ProductSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    name: str  # Campo obligatorio
    description: Optional[str] = None  # Campo opcional
    
    class Config:
        allow_population_by_field_name = True  # Permite usar "id" o "_id"
        json_encoders = {ObjectId: str}  # Convierte ObjectId a str en respuestas JSON
    

class ProductModel(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    content: str
    date: datetime = Field(default_factory=datetime.now)
    important: bool = False

    class Config:
        allow_population_by_field_name = True  # Permite usar "id" o "_id"
        json_encoders = {ObjectId: str}  # Convierte ObjectId a str en respuestas JSON