from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from bson import ObjectId
from typing import Optional

# Convertir ObjectId de MongoDB a String
class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return str(v)

# Modelo de Usuario
class User(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    username: str
    email: EmailStr
    password_hash: str
    role: str = "user"
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Modelo de Tienda
class Store(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    website: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Modelo de Producto
class Product(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str
    category: str
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Modelo de Precio
class Price(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    product_id: str
    store_id: str
    price: float
    scraped_at: datetime = Field(default_factory=datetime.utcnow)
