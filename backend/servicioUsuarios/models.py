from datetime import datetime
from typing import Any, Optional
from bson import ObjectId
from pydantic import BaseModel, Field


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: Any, info: Any = None):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid ObjectId")
        return ObjectId(v)

    @classmethod
    def __get_pydantic_json_schema__(cls, schema: dict[str, Any], _field: Any) -> dict[str, Any]:
        schema.update(type="string")
        return schema

# Modelo Usuario
class Usuario(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias="_id")
    nombre: str
    email: str
    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

