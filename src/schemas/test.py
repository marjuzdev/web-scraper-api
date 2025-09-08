from pydantic import BaseModel, HttpUrl, constr
from typing import Optional

class TestSchema(BaseModel):
    name: constr(min_length=1, max_length=100) # type: ignore
    url_base: HttpUrl
    country: Optional[constr(min_length=2, max_length=2)] # type: ignore