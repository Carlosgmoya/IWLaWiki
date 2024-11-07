from services import wiki as wikiAPI, articulo as articuloAPI

from fastapi import FastAPI, Request, HTTPException, Query
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Any
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
    wikis_json = await wikiAPI.getAllWikis()

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
    
    articulos_json = await articuloAPI.getAllArticulos(obj_id)
    
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
    
    nuevaWiki = await wikiAPI.createWiki(nombre, descripcion)

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



# BORRAR ARTICULO



# EDITAR ARTICULO



# BUSCAR ARTICULOS

@api.get("/searchArt")
async def buscarArticulos(request: Request, term: str = Query(None, min_length=1)):
    return "Por implementar"