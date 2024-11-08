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

api = FastAPI()
api.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# ejecutar con  cd src -> python -m uvicorn main:api --reload --port 8000


# PAGINA PRINCIPAL
@api.get("/", response_class=HTMLResponse)
async def getIndex(request : Request):
    wikis_json = await wikiAPI.getTodasWikis()

    return templates.TemplateResponse(
        "index.html",
        {"request": request,
         "wikis": wikis_json}
    )

# GET WIKI
@api.get("/wiki/{n}", response_class=HTMLResponse)
async def getWiki(request: Request, n : str):
    wiki_json = await wikiAPI.getWiki(n)

    if wiki_json is None:
        raise HTTPException(status_code=404, detail="Wiki no encontrado")

    wiki_dict = wiki_json["_id"]
    wiki_id = wiki_dict["$oid"]

    try:
        obj_id = ObjectId(wiki_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID inválido")
    
    articulos_json = await articuloAPI.getTodosArticulos(obj_id)
    
    return templates.TemplateResponse(
        "wiki.html",
        {"request": request,
         "wiki": wiki_json,
         "articulos": articulos_json}
    )

# CREAR WIKI
@api.post("/wikis")
async def createWiki(request: Request):
    # TODO: sustituir esto por un modelo de pydantic
    data = await request.json()
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    
    nuevaWiki = await wikiAPI.crearWiki(nombre, descripcion)

    return nuevaWiki


# BORRAR WIKI
@api.delete("/delete/{wiki_id}")
async def eliminarWiki(wiki_id: str):
    try:
        obj_id = ObjectId(wiki_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID inválido")
    
    result = await wikiAPI.eliminarWiki(obj_id)

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Wiki no encontrada")

    return "Wiki eliminada con éxito"


# EDITAR WIKI
@api.put("/edit/{wiki_id}")
async def actualizarWiki(request: Request, wiki_id: str):
    try:
        obj_id = ObjectId(wiki_id)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    
    # TODO: sustituir esto por un modelo de pydantic
    data = await request.json()
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    
    result = await wikiAPI.actualizarWiki(obj_id, nombre, descripcion)
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Wiki no encontrada")
    
    if result.modified_count == 0:
        return "No se realizaron cambios"
    
    return "Wiki actualizada con éxito"


# BUSCAR WIKIS

@api.get("/search")
async def buscarWikis(request: Request, term: str = Query(None, min_length=1)):
    wikis_json = await wikiAPI.buscarWikis(term)
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request,
         "wikis": wikis_json}
    )
    
# GET ARTICULO

@api.get("/wiki/{n}/{t}", response_class=HTMLResponse)
async def getArticulo(request: Request, n : str, t : str):
    articulo_json = await articuloAPI.getArticulo(t)

    if articulo_json is None:
        raise HTTPException(status_code=404, detail="Item not found")

    return templates.TemplateResponse(
        "articulo.html",
        {"request": request,
         "articulo": articulo_json}
    )


# CREAR ARTICULO

@api.post("/wiki/{n}")
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


# BORRAR ARTICULO



# EDITAR ARTICULO



# BUSCAR ARTICULOS

@api.get("/wiki/{n}/buscar/bien", response_class=HTMLResponse)
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

    return templates.TemplateResponse(
        "wiki.html",
        {"request": request,
         "wiki": wiki_json,
         "articulos": articulos_json}
    )