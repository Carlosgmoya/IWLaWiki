from services import wiki as wikiAPI, articulo as articuloAPI

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

#   -ejecutar de manera local -> python -m uvicorn main:api --reload --port 8002

# prefijo para todas las URLs


api = FastAPI()

# GET ARTICULO

@api.get("/wikis/{n}/articulos/{t}")
async def getArticulo(n : str, t : str):
    articulo_json = await articuloAPI.getArticulo(t)

    if articulo_json is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return articulo_json

# GET ARTICULOS DE UNA WIKI

@api.get("/wikis/{n}/articulos")
async def getArticulos(n: str):

    wiki_json = await solicitarWiki(n)
    wiki_dict = wiki_json["_id"]
    wiki_id = wiki_dict["$oid"]

    try:
        obj_id = ObjectId(wiki_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID inválido")
    
    articulos_json = await articuloAPI.getTodosArticulos(obj_id)

    return articulos_json

# CREAR ARTICULO

@api.post("/wikis/{n}/articulos/{t}")
async def crearArticulo(request: Request, n: str, t: str):

    data = await request.json()
    titulo = t
    wiki_id = data.get("wiki")
    wiki_object_id = ObjectId(wiki_id)
    contenido = data.get("contenido")
    creador = data.get("creador")

    wiki_json = await solicitarWiki(n)

    wiki_dict = wiki_json["_id"]
    wiki_id = wiki_dict["$oid"]

    try:
        obj_id = ObjectId(wiki_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID inválido")
    
    if obj_id != wiki_object_id:
        raise HTTPException(status_code=400, detail="Los IDs no coinciden")
   
    nuevoArticulo = await articuloAPI.crearArticulo(titulo, wiki_object_id, contenido,creador)

    return nuevoArticulo


# BORRAR UNA VERSIÓN DEL ARTÍCULO

@api.delete("wikis/{wiki_id}/{articulo_id}")
async def eliminarTodasVersionesArticulo(wiki_id: str, articulo_id: str):
    try:
        obj_id = ObjectId(wiki_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID de wiki inválido")
    
    try:
        obj_id = ObjectId(articulo_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID de artículo inválido")
    
    result = await articuloAPI.eliminarVersionArticulo(obj_id)

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Versión del artículo no encontrada")

    return f"Versión del artículo eliminada con éxito"


# BORRAR TODAS LAS VERSIONES DE UN ARTICULO

@api.delete("/wikis/{n}/articulos/{t}")
async def eliminarTodasLasVersionesDeUnArticulo(n: str, t: str):
    result = await articuloAPI.eliminarTodasVersionesArticulo(t)

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Artículo {t} no encontrado")

    return f"Artículo {t} eliminado con éxito"


# BUSCAR ARTICULOS

@api.get("/wikis/{n}/buscar/bien")
async def filtrarArticulosPorContenido(request: Request, n: str, term: Union[str, None] = Query(None)):
    wiki_json = await wikiAPI.getWiki(n)
    if wiki_json is None:
        raise HTTPException(status_code=404, detail="Wiki no encontrado")
    wiki_dict = wiki_json["_id"]
    wiki_id = wiki_dict["$oid"]
    id = ObjectId(wiki_id)
    articulos_json = await articuloAPI.buscarArticulos(term, id)
    if not articulos_json:
        raise HTTPException(status_code=404, detail="No se encontraron artículos que coincidan con el contenido")

    return articulos_json

@api.get("/wikis/{n}/ordenado/bien", response_class=HTMLResponse)
async def buscarPorUsuarioOrdeando(request: Request, n: str, term: Union[str, None] = Query(None)):
    wiki_json = await wikiAPI.getWiki(n)
    wiki_dict = wiki_json["_id"]
    wiki_id = wiki_dict["$oid"]
    id = ObjectId(wiki_id)

    articulos_json = await articuloAPI.buscarUsuarioOrdenado(term, id)
    return articulos_json



########## Metodos Complementarios ############

async def solicitarWiki(nombreWiki: str):
    url = f"http://localhost:8001/wikis/{nombreWiki}"

    # Realizar la solicitud HTTP asíncrona
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
    
    # Comprobar si la solicitud fue exitosa
    if response.status_code != 200:
        raise HTTPException(status_code=response.status_code, detail="Error al obtener el artículo")

    # Procesar la respuesta
    wiki_json = response.json()

    if wiki_json is None:
        raise HTTPException(status_code=404, detail="Wiki no encontrado")

    return wiki_json

