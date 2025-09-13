from pydantic import BaseModel, HttpUrl, constr, conint
from typing import Optional

class PriceHistoryCreateSchema(BaseModel):
    name: constr(min_length=1, max_length=100) # type: ignore
    url_base: HttpUrl
    country: constr(min_length=2, max_length=2) # type: ignore

class PriceHistoryUpdateSchema(BaseModel):
    name: Optional[constr(min_length=1, max_length=100)] # type: ignore
    url_base: Optional[HttpUrl]
    country: Optional[constr(min_length=2, max_length=2)] # type: ignore

    class Config:
        extra = "forbid"


class PriceHistoryFilterSchema(BaseModel):
    name: Optional[constr(min_length=1)] = None # type: ignore
    country: Optional[constr(min_length=2, max_length=2)] = None # type: ignore
    limit: Optional[conint(gt=0, le=100)] = 50  # type: ignore # default 50
