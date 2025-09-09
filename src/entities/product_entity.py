from beanie import Document
from pydantic import Field
from datetime import datetime, timezone

# class ProductEntity(Document):
#     name: str
#     brand: str
#     category: str
#     created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
#     updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

#     class Settings:
#         name = "products"

class ProductEntity(Document):
    name: str
    brand: str
    category: str
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "products"
