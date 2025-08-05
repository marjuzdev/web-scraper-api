from datetime import datetime, timezone
from typing import Optional
from bson import ObjectId
from pydantic import BaseModel, Field
from schemas.custom_types import BaseSchema, PyObjectId

class CssSelectors(BaseModel):
    price_normal: str = Field(...)
    price_discount: Optional[str] = Field(None)

class MarketplaceSchema(BaseSchema):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")
    name: str = Field(...)
    url_base: str = Field(...)
    country: Optional[str] = Field(None)
    css_selectors: CssSelectors = Field(...)
    created_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: Optional[datetime] = Field(default_factory=lambda: datetime.now(timezone.utc))


class MarketplaceUpdateSchema(BaseModel):
    name: Optional[str] = None
    url_base: Optional[str] = Field(None)
