from services import articulo as articuloAPI

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

api = FastAPI()

# prefijo para todas las URLs
path = "/api/v1"

#   -ejecutar de manera local -> python -m uvicorn main:api --reload --port 8002


# GET ARTICULOS DE UNA WIKI
@api.get(path + "/wikis/{nombre}/articulos")
async def getArticulos(request: Request, nombre: str):
    wikiJSON = await solicitarWiki(nombre)
    objID = getWikiObjID(wikiJSON)

    #if term contiene el campo terminoDeBusqueda -> articuloAPI.getArticulosPorTituloYContenido(objID, terminoDeBusqueda)
    #if term contiene el campo usuario -> articuloAPI.getArticulosPorUsuarioOrdenado(objID, usuario)
    try:
        filters = await request.json()
    except Exception as e:
        filters = {}
    
    if not filters:
        articulosJSON = await articuloAPI.getTodosArticulos(objID)
    elif "terminoDeBusqueda" in filters:
        articulosJSON = await articuloAPI.getArticulosPorTituloYContenido(objID, filters["terminoDeBusqueda"])
    elif "usuario" in filters:
        articulosJSON = await articuloAPI.getArticulosPorUsuarioOrdenadoPorFecha(objID, filters["usuario"]) # se accede a la base de datos de usuario desde aqui porque aun no se ha implementado el modulo "usuario"
    
    return articulosJSON


# GET ARTICULO
@api.get(path + "/wikis/{nombre}/articulos/{titulo}")
async def getArticulo(nombre : str, titulo : str):
    wikiJSON = await solicitarWiki(nombre)
    objID = getWikiObjID(wikiJSON)
    
    articulo_json = await articuloAPI.getArticulo(objID, titulo)

    if articulo_json is None:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
    
    return articulo_json


# CREAR ARTICULO
@api.post(path + "/wikis/{nombre}/articulos")
async def crearArticulo(request: Request, nombre: str):
    wikiJSON = await solicitarWiki(nombre)
    
    try:
        data = await request.json()
    except Exception as e:
        data = {}

    if not data:
        raise HTTPException(status_code=400, detail="Parametros de request vacío")
    
    titulo = data.get("titulo")
    wiki = getWikiObjID(wikiJSON)
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
async def actualizarArticulo(request: Request, nombre: str, titulo: str):
    wikiJSON = await solicitarWiki(nombre)

    try:
        data = await request.json()
    except Exception as e:
        data = {}

    if not data:
        raise HTTPException(status_code=400, detail="Parametros de request vacío")
    
    wiki = getWikiObjID(wikiJSON)
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
    result = None

    if id is None:
        result = await articuloAPI.eliminarTodasVersionesArticulo(titulo)
    else:
        objID = ObjectId(id)
        result = await articuloAPI.eliminarVersionArticulo(objID)
        

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Versión del artículo no encontrada")

    return "Artículo eliminado con éxito"


########## Metodos Complementarios ############

async def solicitarWiki(nombreWiki: str):
    url = f"http://localhost:8001/api/v1/wikis/{nombreWiki}"

    # Realizar la solicitud HTTP asíncrona
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    # Comprobar si la solicitud fue exitosa
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener el artículo")

    # Procesar la respuesta
    wikiJSON = response.json()

    if wikiJSON is None:
        raise HTTPException(status_code=404, detail="Wiki no encontrado")

    return wikiJSON

def getWikiObjID(wikiJSON: json):
    wikiDict = wikiJSON["_id"]
    wikiID = wikiDict["$oid"]

    try:
        objID = ObjectId(wikiID)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID de wiki inválido")
    
    return objID

