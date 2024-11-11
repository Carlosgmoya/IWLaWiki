from services import wiki as wikiAPI

from fastapi import FastAPI, Request, HTTPException, Query

from typing import Any, Union
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime
from fastapi.middleware.cors import CORSMiddleware



app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Cambia al puerto de tu frontend en React
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# prefijo para todas las URLs
path = "/api/v1"

# Desde el directorio de este archivo: 2 maneras de ejecutar la app:
#   -ejecutar de manera local -> python -m uvicorn main:api --reload --port 8001
#   -ejecutar el contenedor Docker -> docker run -p 8001:8001 fu17alex/modulowiki:v1.0


# PAGINA PRINCIPAL: DEVUELVE TODAS LAS WIKIS O DEVUELVE LAS WIKIS QUE CUMPLEN UNOS CRITERIOS
@app.get(path + "/wikis")
async def getWikis(term: str = Query(None, min_length=1)):  #SOLO ES UN ESQUEMA, FALTA POR IMPLEMENTAR
    return await wikiAPI.getTodasWikis() if term is None else await wikiAPI.getWikisPorNombre(term)


# PAGINA WIKI
@app.get(path + "/wikis/{nombre}")
async def getWiki(nombre: str):
    wikiJSON = await wikiAPI.getWiki(nombre)

    if wikiJSON is None:
        raise HTTPException(status_code=404, detail="Wiki no encontrado")
    
    return wikiJSON
    
    
# CREAR WIKI
@app.post(path + "/wikis")
async def crearWiki(request: Request):
    data = await request.json()
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")

    wikiJSON = await wikiAPI.getWiki(nombre)

    return await wikiAPI.crearWiki(nombre, descripcion) if wikiJSON is None else "Ya existe una wiki con ese nombre"


# ACTUALIZAR WIKI
@app.put(path + "/wikis/{wikiID}")
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
@app.delete(path + "/wikis/{wikiID}")
async def eliminarWiki(wikiID: str):
    try:
        obj_id = ObjectId(wikiID)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID inválido")
    
    result = await wikiAPI.eliminarWiki(obj_id)

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Wiki no encontrada")

    return "Wiki eliminada con éxito"