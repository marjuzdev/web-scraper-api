from bson import ObjectId
from pydantic import BaseModel
from pydantic_core import core_schema
from typing import Any
from datetime import datetime

class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(cls, _source_type: Any, _handler: Any) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.no_info_plain_validator_function(cls.validate),
            serialization=core_schema.plain_serializer_function_ser_schema(str),
        )

    @classmethod
    def validate(cls, v: Any) -> ObjectId:
        if not ObjectId.is_valid(v):
            raise ValueError(f"Invalid ObjectId: {v}")
        return ObjectId(v)

class BaseSchema(BaseModel):
    model_config = {
        "populate_by_name": True,
        "arbitrary_types_allowed": True,
        "json_encoders": {
            ObjectId: str,
            datetime: lambda v: v.isoformat(),
        },
    }
