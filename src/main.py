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

# conexion al servidor MongoDB

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.mw2bq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Base de Datos

database = client["laWiki"]

BD_wiki = database["wiki"]
BD_articulo = database["articulo"]

# PAGINA PRINCIPAL
@api.get("/", response_class=HTMLResponse)
async def getIndex(request : Request):
    wikis_doc = BD_wiki.find().sort({"nombre":1})
    wikis_json = [json.loads(json_util.dumps(doc)) for doc in wikis_doc]    # collection.find() retrieves documents in BSON format from MongoDB.
                                                                            # json_util.dumps(doc) converts BSON documents, including ObjectId fields, to JSON strings.
                                                                            # json.loads(...) transforms each document back into a Python dictionary, so it’s compatible with FastAPI's JSON response model.
    return templates.TemplateResponse(
        "index.html",
        {"request": request,
         "wikis": wikis_json}
    )

# GET WIKI
@api.get("/wiki/{n}", response_class=HTMLResponse)
async def getWiki(request: Request, n : str):
    wiki_doc = BD_wiki.find_one({ "nombre" : n })
    if wiki_doc is None:
        raise HTTPException(status_code=404, detail="Wiki no encontrado")
    wiki_json = json.loads(json_util.dumps(wiki_doc))

    articulos_doc = BD_articulo.find({"wiki": n})
    articulos_json = json.loads(json_util.dumps(articulos_doc))

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
    fecha = datetime.utcnow()
    nuevaWiki = {
        "nombre": nombre,
        "fecha": fecha,
        "descripcion": descripcion
    }
    
    result = BD_wiki.insert_one(nuevaWiki)
    # devolvemos la nueva wiki al cliente, incluyendo la ID
    nuevaWiki["_id"] = str(result.inserted_id)
    return nuevaWiki


# BORRAR WIKI
@api.delete("/delete/{wiki_id}")
async def eliminarWiki(wiki_id: str):
    try:
        obj_id = ObjectId(wiki_id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID inválido")
    
    result = BD_wiki.delete_one({"_id": obj_id})

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
    
    result = BD_wiki.update_one({"_id": obj_id},
                                {"$set":
                                 {"nombre": nombre,
                                 "descripcion": descripcion}
                                })
    
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Wiki no encontrada")
    
    if result.modified_count == 0:
        return "No se realizaron cambios"
    
    return "Wiki actualizada con éxito"


# BUSCAR WIKIS

@api.get("/search")
async def buscarWikis(request: Request, term: str = Query(None, min_length=1)):
    wikis_doc = BD_wiki.find({"nombre": {"$regex": term, "$options": "i"}})
    wikis_json = [json.loads(json_util.dumps(doc)) for doc in wikis_doc]
    
    return templates.TemplateResponse(
        "index.html",
        {"request": request,
         "wikis": wikis_json}
    )
    
# GET ARTICULO

@api.get("/wiki/{n}/{t}", response_class=HTMLResponse)
async def getWiki(request: Request, n : str, t : str):
    articulo_doc = BD_articulo.find_one({ "titulo" : t })

    if articulo_doc is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    articulo_json = json.loads(json_util.dumps(articulo_doc))

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