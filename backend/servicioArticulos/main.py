from services import articulo as articuloAPI

from fastapi import FastAPI, Request, HTTPException, Query

from typing import Any
from bson.objectid import ObjectId
from typing import List
import json
from fastapi.middleware.cors import CORSMiddleware
import re

api = FastAPI()

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

#   -ejecutar de manera local -> python -m uvicorn main:api --reload --port 8002


def getObjID(id: str):
    try:
        objID = ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID de wiki inválido")

    return objID


# GET ARTICULOS DE UNA WIKI
@api.get(path + "/wikis/{nombre}/articulos")
async def getArticulos(nombre: str, terminoDeBusqueda: str | None = None, usuario: str | None = None, wiki: str = Query(...)):
    wikiObjID = getObjID(wiki)

    if terminoDeBusqueda is not None:
        articulosJSON = await articuloAPI.getArticulosPorTituloYContenido(wikiObjID, terminoDeBusqueda)
    elif usuario is not None:
        articulosJSON = await articuloAPI.getArticulosPorUsuarioOrdenadoPorFecha(wikiObjID, usuario) # se accede a la base de datos de usuario desde aqui porque aun no se ha implementado el modulo "usuario"
    else:
        articulosJSON = await articuloAPI.getTodosArticulos(wikiObjID)

    return articulosJSON


# GET ARTICULO
@api.get(path + "/wikis/{nombre}/articulos/{titulo}")
async def getArticulo(nombre : str, titulo : str, wiki: str = Query(...)):
    wikiObjID = getObjID(wiki)
    
    articulo_json = await articuloAPI.getArticulo(wikiObjID, titulo)

    if articulo_json is None:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
     # Formatear el contenido de cada artículo
    articulo_json["contenido"] = formatearContenido(articulo_json["contenido"])
    
    return articulo_json


# CREAR ARTICULO
@api.post(path + "/wikis/{nombre}/articulos")
async def crearArticulo(request: Request, nombre: str, wiki: str = Query(...)):
    wikiObjID = getObjID(wiki)
    
    try:
        data = await request.json()
    except Exception as e:
        data = {}

    if not data:
        raise HTTPException(status_code=400, detail="Parametros de request vacío")
    
    titulo = data.get("titulo")
    wiki = wikiObjID
    contenido = data.get("contenido")
    creador = data.get("creador")
    if isinstance(creador, dict) and "$oid" in creador:
        creador = ObjectId(creador["$oid"])  # Convert the string inside "$oid" to ObjectId

    # If 'creador' is already an ObjectId string or directly an ObjectId
    elif isinstance(creador, str):
        creador = ObjectId(creador)

    articuloJSON = await articuloAPI.getArticulo(wiki, titulo)
   
    return await articuloAPI.crearArticulo(titulo, wiki, contenido, creador) if articuloJSON is None else "Ya existe articulo con ese nombre"


# ACTUALIZAR UN ARTÍCULO
@api.put(path + "/wikis/{nombre}/articulos/{titulo}")
async def actualizarArticulo(request: Request, nombre: str, titulo: str, wiki: str = Query(...)):
    wikiObjID = getObjID(wiki)

    try:
        data = await request.json()
    except Exception as e:
        data = {}

    if not data:
        raise HTTPException(status_code=400, detail="Parametros de request vacío")
    
    wiki = wikiObjID
    contenido = data.get("contenido")
    creador = data.get("creador")
    if isinstance(creador, dict) and "$oid" in creador:
        creador = ObjectId(creador["$oid"])  # Convert the string inside "$oid" to ObjectId

    # If 'creador' is already an ObjectId string or directly an ObjectId
    elif isinstance(creador, str):
        creador = ObjectId(creador)

    result = await articuloAPI.actualizarArticulo(titulo, wiki, contenido, creador)

    return result

# BORRAR UNA TODAS LAS VERSIONES DEL ARTÍCULO O SOLO UNA VERSION SI SE PASA ID
@api.delete(path + "/wikis/{nombre}/articulos/{titulo}")
async def eliminarArticulo(nombre: str, titulo: str, id: str = Query(None, min_length=1)):
    if id is None:
        result = await articuloAPI.eliminarTodasVersionesArticulo(titulo)
    else:
        wikiObjID = getObjID(id)
        result = await articuloAPI.eliminarVersionArticulo(wikiObjID)
        

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Versión del artículo no encontrada")

    return "Artículo eliminado con éxito"


########## Metodos Complementarios ############


def getWikiObjID(wikiJSON: json):
    wikiDict = wikiJSON["_id"]
    wikiID = wikiDict["$oid"]

    try:
        objID = ObjectId(wikiID)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID de wiki inválido")
    
    return objID

def formatearContenido(contenido):
    patron_titulo = r"==\s*(.+?)\s*=="
    partes = re.split(patron_titulo, contenido)
    
    contenido_formateado = []
    for i in range(1, len(partes), 2):
        subtitulo = partes[i].strip()
        cuerpo = partes[i + 1].strip()
        contenido_formateado.append({
            "subtitulo": subtitulo,
            "cuerpo": cuerpo
        })
    return contenido_formateado