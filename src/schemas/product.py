from pydantic import BaseModel, Field
from typing import Optional

class ProductSchema(BaseModel):
    name: str  # Campo obligatorio
    description: Optional[str] = None  # Campo opcional
