#ejecutar de manera local -> python -m uvicorn main:api --reload --port 8004
from fastapi import FastAPI, Request, HTTPException, Query

from typing import Any, Union
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime
import httpx
from fastapi.middleware.cors import CORSMiddleware

from models import Usuario, Valoracion
from bd import usuarioBD, valoracionBD

# prefijo para todas las URLs
path = "/api/v1"

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

######## USUARIOS ########

@api.get(path + "/usuarios", response_model=List[Usuario])
async def getUsuarios():
    """Devuelve todos los usuarios."""
    usuarios = list(usuarioBD.find())
    return [Usuario(**usuario) for usuario in usuarios]

@api.get(path + "/usuarios/id/{usuario_id}", response_model=Usuario)
async def getUsuariosPorId(usuario_id: str):
    """Busca un usuario por su id"""
    usuario = usuarioBD.find_one({"_id": ObjectId(usuario_id)})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return Usuario(**usuario)

@api.get(path + "/usuarios/email/{usuario_email}", response_model=Usuario)
async def getUsuariosPorEmail(usuario_email: str):
    """Busca un usuario por su id"""
    usuario = usuarioBD.find_one({"email": usuario_email})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return Usuario(**usuario)

@api.post(path + "/usuarios", response_model=Usuario)
async def crearUsuario(usuario: Usuario):
    """Crea un nuevo usuario"""
    usuario_dict = usuario.dict(by_alias=True)
    resultado = usuarioBD.insert_one(usuario_dict)
    usuario_dict["_id"] = resultado.inserted_id
    return Usuario(**usuario_dict)

######## VALORACIONES ########

@api.get(path + "/valoraciones", response_model=List[Valoracion])
async def getValoraciones():
    """Devuelve todas las valoraciones"""
    valoraciones = list(valoracionBD.find())
    return [Valoracion(**valoracion) for valoracion in valoraciones]

@api.post(path + "/valoraciones", response_model=Valoracion)
async def crearValoracion(valoracion: Valoracion):
    """Crea una nueva valoración. Para evitar que un mismo usuario no
    valore a otro muchas veces, solo se guardará la valoración más reciente"""
    valoracion_dict = valoracion.dict(by_alias=True)

    filtro = {
        "de_usuario": valoracion_dict["de_usuario"],
        "a_usuario": valoracion_dict["a_usuario"]
    }

    #si ya existe una valoracion con los mismos usuarios, borrarla
    valoracionBD.delete_one(filtro)

    resultado = valoracionBD.insert_one(valoracion_dict)
    valoracion_dict["_id"] = resultado.inserted_id
    return Valoracion(**valoracion_dict)


@api.get(path + "/valoraciones/de/{usuario_email}", response_model=List[Valoracion])
async def getValoracionesDeUsuario(usuario_email: str):
    """Devuelve todas las valoraciones hechas por un usuario"""
    valoraciones = list(valoracionBD.find({"de_usuario": usuario_email}))
    return [Valoracion(**valoracion) for valoracion in valoraciones]

@api.get(path + "/valoraciones/a/{usuario_email}", response_model=List[Valoracion])
async def getValoracionesDeUsuario(usuario_email: str):
    """Devuelve todas las valoraciones dirigidas a un usuario"""
    valoraciones = list(valoracionBD.find({"a_usuario": usuario_email}))
    return [Valoracion(**valoracion) for valoracion in valoraciones]

@api.get(path + "/valoracion/{usuario_email}")
async def getValoracionDeUsuario(usuario_email: str):
    """Devuelve la media de las valoraciones de un usuario, o 0 si no tiene"""
    valoraciones = list(valoracionBD.find({"a_usuario": usuario_email}))
    if len(valoraciones) == 0:
        return {"valor": 0}
    suma = 0
    for valoracion in valoraciones:
        suma += valoracion["valor"]
    media = suma / len(valoraciones)    
    return {"valor": media}

