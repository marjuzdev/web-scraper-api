from beanie import Document
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, timezone

class CssSelectors(BaseModel):
    price_normal: str = Field(...)
    price_discount: Optional[str] = Field(None)

class MarketplaceEntity(Document):
    name: str
    url_base: str
    country: Optional[str] = None
    css_selectors: CssSelectors
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "marketplaces"
