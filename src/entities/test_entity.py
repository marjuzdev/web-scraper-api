
from beanie import Document
from pydantic import Field
from typing import Optional
from datetime import datetime, timezone

class TestEntity(Document):
    name: str
    url_base: str
    country: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))

    class Settings:
        name = "test"