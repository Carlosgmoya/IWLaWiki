#ejecutar de manera local -> python -m uvicorn main:api --reload --port 8004
from fastapi import FastAPI, HTTPException
from bson.objectid import ObjectId
from typing import List
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

@api.get(path + "/usuarios/id/{usuarioId}", response_model=Usuario)
async def getUsuariosPorId(usuarioId: str):
    """Busca un usuario por su id"""
    usuario = usuarioBD.find_one({"_id": ObjectId(usuarioId)})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return Usuario(**usuario)

@api.get(path + "/usuarios/email/{usuarioEmail}", response_model=Usuario)
async def getUsuariosPorEmail(usuarioEmail: str):
    """Busca un usuario por su email"""
    usuario = usuarioBD.find_one({"email": usuarioEmail})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return Usuario(**usuario)

@api.get(path + "/usuarios/nombre/{usuarioNombre}", response_model=Usuario)
async def getUsuariosPorNombre(usuarioNombre: str):
    """Busca un usuario por su email"""
    usuario = usuarioBD.find_one({"nombre": usuarioNombre})
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return Usuario(**usuario)

@api.post(path + "/usuarios", response_model=Usuario)
async def crearUsuario(usuario: Usuario):
    """Crea un nuevo usuario"""
    usuarioDict = usuario.dict(by_alias=True)
    # comprobar si un usuario con el mismo nombre ya existe
    usuarioExistente = usuarioBD.find_one({"nombre": usuarioDict["nombre"]})
    if usuarioExistente:
        raise HTTPException(status_code=409, detail="El nombre de usuario ya existe")
    resultado = usuarioBD.insert_one(usuarioDict)
    usuarioDict["_id"] = resultado.inserted_id
    return Usuario(**usuarioDict)

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
    valoracionDict = valoracion.dict(by_alias=True)

    filtro = {
        "de_usuario": valoracionDict["de_usuario"],
        "a_usuario": valoracionDict["a_usuario"]
    }

    #si ya existe una valoracion con los mismos usuarios, borrarla
    valoracionBD.delete_one(filtro)

    resultado = valoracionBD.insert_one(valoracionDict)
    valoracionDict["_id"] = resultado.inserted_id
    return Valoracion(**valoracionDict)


# ---------- PENDIENTE DE CAMBIAR A NOMBRE DE USUARIO EN LUGAR DE EMAIL ------------- #

@api.get(path + "deprecated/valoraciones/de/{usuarioEmail}", response_model=List[Valoracion])
async def getValoracionesDeUsuariov1(usuarioEmail: str):
    """Devuelve todas las valoraciones hechas por un usuario"""
    valoraciones = list(valoracionBD.find({"de_usuario": usuarioEmail}))
    return [Valoracion(**valoracion) for valoracion in valoraciones]

@api.get(path + "deprecated/valoraciones/a/{usuarioEmail}", response_model=List[Valoracion])
async def getValoracionesDeUsuariov1(usuarioEmail: str):
    """Devuelve todas las valoraciones dirigidas a un usuario"""
    valoraciones = list(valoracionBD.find({"a_usuario": usuarioEmail}))
    return [Valoracion(**valoracion) for valoracion in valoraciones]

@api.get(path + "deprecated/valoracion/{usuarioEmail}")
async def getValoracionDeUsuariov1(usuarioEmail: str):
    """Devuelve la media de las valoraciones de un usuario, o 0 si no tiene"""
    valoraciones = list(valoracionBD.find({"a_usuario": usuarioEmail}))
    if len(valoraciones) == 0:
        return {"valor": 0}
    suma = 0
    for valoracion in valoraciones:
        suma += valoracion["valor"]
    media = suma / len(valoraciones)    
    return {"valor": media}
# ---------------------------------------------------------------------------------------#


@api.get(path + "/valoracion/{usuario}")
async def getValoracionDeUsuario(usuario: str):
    """Devuelve la media de las valoraciones de un usuario, o 0 si no tiene"""
    valoraciones = list(valoracionBD.find({"a_usuario": usuario}))
    if len(valoraciones) == 0:
        return {"valor": 0}
    suma = 0
    for valoracion in valoraciones:
        suma += valoracion["valor"]
    media = suma / len(valoraciones)    
    return {"valor": media}

