from typing import Any
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime
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
    print("Articulo conectado a MongoDB!")
except Exception as e:
    print(e)

# Base de Datos

database = client["laWiki"]
BD_articulo = database["articulo"]


async def getArticulo(t: str):
    articulo_doc = BD_articulo.find_one({ "titulo" : t })    
    articulo_json = json.loads(json_util.dumps(articulo_doc))

    return articulo_json


async def getTodosLosArticulos(wiki_id: ObjectId):
    articulos_doc = BD_articulo.find({"wiki": wiki_id})
    articulos_json = json.loads(json_util.dumps(articulos_doc))

    return articulos_json


async def buscarArticulos(term: str, n: ObjectId):
    articulos_doc = BD_articulo.find({"contenido": {"$regex": term, "$options": "i"},
                                      "wiki": n})
    articulos_json = [json.loads(json_util.dumps(doc)) for doc in articulos_doc]
    
    return articulos_json

async def buscarVersionPorFecha(titulo: str, fecha: datetime):
    articulo_doc = BD_articulo.find_one({"titulo" : titulo, "fecha" : fecha})
    articulo_json = json.loads(json_util.dumps(articulo_doc))
    return articulo_json

async def crearArticulo(t: str, wiki_id: ObjectId, c: str):
    fecha = datetime.utcnow()
    nuevoArticulo = {
        "titulo": t,
        "wiki": wiki_id,
        "fecha": fecha,
        "ultimoModificado": True,
        "contenido": c
    }
    result = BD_articulo.insert_one(nuevoArticulo)
    nuevoArticulo["_id"] = str(result.inserted_id)
    nuevoArticulo["wiki"] = str(wiki_id)
    
    return nuevoArticulo

async def eliminarVersionArticulo(articulo_id: ObjectId):
    result = BD_articulo.delete_one({"_id": articulo_id})
    return result

async def eliminarTodasVersionesArticulo(titulo: str):
    result = BD_articulo.delete_many({"titulo": titulo})
    return result

#Modificar un articulo seria crear uno nuevo
