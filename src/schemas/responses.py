from typing import Generic, TypeVar, Optional, Dict

from pydantic.generics import GenericModel
T = TypeVar("T")

class ResponseModel(GenericModel, Generic[T]):
    success: bool = True
    message: str
    data: Optional[T] = None
    errors: Optional[Dict] = None


