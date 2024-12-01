#ejecutar de manera local -> python -m uvicorn main:api --reload --port 8004
from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Any, Union
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime
import httpx
from fastapi.middleware.cors import CORSMiddleware

from models import Usuario
from bd import usuarioBD

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

