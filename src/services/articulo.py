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

async def getAllArticulos(wiki_id: ObjectId):
    articulos_doc = BD_articulo.find({"wiki": wiki_id})
    articulos_json = json.loads(json_util.dumps(articulos_doc))

    return articulos_json