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
    esAdmin: bool
    class Config:
        json_encoders = {ObjectId: str}
        populate_by_name = True

# Modelo Valoracion
class Valoracion(BaseModel):
    id: Optional[PyObjectId] = Field(default_factory=ObjectId, alias="_id")
    de_usuario: str # email del usuario que pone la valoración
    a_usuario: str # email del usuario al que va dirigida la valoración
    valor: int # valoracion entre 1 y 5 estrellas
    class Config:
        json_encoders = {ObjectId: str}
        allow_population_by_field_name = True