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
    print("Wiki conectado a MongoDB!")
except Exception as e:
    print(e)

# Base de Datos

database = client["laWiki"]

BD_wiki = database["wiki"]


async def getWiki(n : str):
    wiki_doc = BD_wiki.find_one({ "nombre" : n })
    wiki_json = json.loads(json_util.dumps(wiki_doc))

    return wiki_json


async def getWikiById(id: ObjectId):
    wiki_doc = BD_wiki.find_one({ "_id": id })
    wiki_json = json.loads(json_util.dumps(wiki_doc))

    return wiki_json


async def getAllWikis():
    wikis_doc = BD_wiki.find().sort({"nombre":1})
    wikis_json = [json.loads(json_util.dumps(doc)) for doc in wikis_doc]    # collection.find() retrieves documents in BSON format from MongoDB.
                                                                            # json_util.dumps(doc) converts BSON documents, including ObjectId fields, to JSON strings.
                                                                            # json.loads(...) transforms each document back into a Python dictionary, so it’s compatible with FastAPI's JSON response model.
    return wikis_json


async def createWiki(nombre: str, descripcion: str):
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


async def eliminarWiki(wiki_id: ObjectId):
    
    result = BD_wiki.delete_one({"_id": wiki_id})

    return result


async def actualizarWiki(wiki_id: ObjectId, nombre: str, descripcion: str):
    result = BD_wiki.update_one({"_id": wiki_id},
                                {"$set":
                                 {"nombre": nombre,
                                 "descripcion": descripcion}
                                })
    return result



async def buscarWikis(term: str):
    wikis_doc = BD_wiki.find({"nombre": {"$regex": term, "$options": "i"}})
    wikis_json = [json.loads(json_util.dumps(doc)) for doc in wikis_doc]
    
    return wikis_json