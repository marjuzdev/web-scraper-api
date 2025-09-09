from beanie import Document
from pydantic import Field
from datetime import datetime, timezone
from schemas.custom_types import PyObjectId
from typing import Optional

class PriceHistoryEntity(Document):
    product_market_id: PyObjectId = Field(...)
    price_normal: float
    price_discount: Optional[float] = None
    currency: str = Field(default="COP")
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "price_history"