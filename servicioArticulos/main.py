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

# prefijo para todas las URLs
path = "/api/v1"

api = FastAPI()

# GET ARTICULO

@api.get("/wiki/{n}/{t}")
async def getArticulo(request: Request, n : str, t : str):
    articulo_json = await articuloAPI.getArticulo(t)

    if articulo_json is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return articulo_json


# CREAR ARTICULO

@api.post(path + "/wikis/{n}")
async def crearArticulo(request: Request, n: str):
    # TODO: sustituir esto por un modelo de pydantic
    data = await request.json()
    titulo = data.get("titulo")
    wiki_id = data.get("wiki")
    wiki_object_id = ObjectId(wiki_id)
    contenido = data.get("contenido")

    wiki = await wikiAPI.getWikiPorId(wiki_object_id)
    if wiki is None:
        raise HTTPException(status_code=404, detail="No existe una wiki con la ID introducida.")
    elif wiki.get("nombre") != n:
        raise HTTPException(status_code=400, detail=f"La wiki solicitada no tiene el nombre {n}.")
    else:
        nuevoArticulo = await articuloAPI.crearArticulo(titulo, wiki_object_id, contenido)

    return nuevoArticulo


# BORRAR UNA VERSIÓN DEL ARTÍCULO

@api.delete(path + "/delete/{wiki_id}/{articulo_id}")
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


# BORRAR TODAS LAS VERSIONES DEL ARTICULO

@api.delete(path + "/delete/{wiki_id}/{titulo}/all")
async def eliminarTodasVersionesArticulo(wiki_id: str, titulo: str):
    try:
        obj_id = ObjectId(wiki_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID de wiki inválido")
    
    result = await articuloAPI.eliminarTodasVersionesArticulo(titulo)

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Artículo {titulo} no encontrado")

    return f"Artículo {titulo} eliminado con éxito"


# EDITAR ARTICULO



# BUSCAR ARTICULOS

@api.get(path + "/wiki/{n}/buscar/bien")
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

@api.get(path + "/wiki/{n}/ordenado/bien", response_class=HTMLResponse)
async def buscarPorUsuarioOrdeando(request: Request, n: str, term: Union[str, None] = Query(None)):
    wiki_json = await wikiAPI.getWiki(n)
    wiki_dict = wiki_json["_id"]
    wiki_id = wiki_dict["$oid"]
    id = ObjectId(wiki_id)

    articulos_json = await articuloAPI.buscarUsuarioOrdenado(term, id)
    return articulos_json