from beanie import Document
from pydantic import Field
from datetime import datetime, timezone
from schemas.custom_types import PyObjectId

class ProductMarketEntity(Document):
    product_id: PyObjectId = Field(...)
    marketplace_id: PyObjectId = Field(...)
    url: str
    available: str = Field(default="yes")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "product_market"
