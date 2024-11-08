from services import wiki as wikiAPI

from fastapi import FastAPI, Request, HTTPException, Query

from typing import Any, Union
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime

api = FastAPI()

# ejecutar con  cd servicioWikis -> python -m uvicorn main:api --reload --port 8001

# PAGINA PRINCIPAL: DEVUELVE TODAS LAS WIKIS O DEVUELVE LAS WIKIS QUE CUMPLEN UNOS CRITERIOS
@api.get("/wikis")
async def getWikis(term: str = Query(None, min_length=1)):  #SOLO ES UN ESQUEMA, FALTA POR IMPLEMENTAR
    if term is None
        return await wikiAPI.getWikis()
    
    return await wikiAPI.buscarWikis(term)


# PAGINA WIKI
@api.get("/wikis/{nombre}")
async def getWiki(nombre: str):
    wiki_json = await wikiAPI.getWiki(nombre)

    if wiki_json is None:
        raise HTTPException(status_code=404, detail="Wiki no encontrado")
    
    return wiki_json
    
    
# CREAR WIKI
@api.post("/wikis")
async def crearWiki(request: Request):
    data = await request.json()
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    return await wikiAPI.createWiki(nombre, descripcion)


# ACTUALIZAR WIKI
@api.put("/wikis/{wikiID}")
async def actualizarWiki(request: Request, wikiID: str):
    try:
        ObjID = ObjectId(wikiID)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    
    # TODO: sustituir esto por un modelo de pydantic
    data = await request.json()
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    
    result = await wikiAPI.actualizarWiki(ObjID, nombre, descripcion)
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Wiki no encontrada")
    
    if result.modified_count == 0:
        return "No se realizaron cambios"
    
    return "Wiki actualizada con éxito"


# ELIMINAR WIKI
@api.delete("/wikis/{wikiID}")
async def eliminarWiki(wikiID: str):
    return None