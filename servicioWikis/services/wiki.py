from typing import Any
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime


# conexion al servidor MongoDB

import bd
wikiBD = bd.wikiBD

# ejecutar con  cd src -> python -m uvicorn main:api --reload --port 8000

async def getWiki(n : str):
    wiki_doc = wikiBD.find_one({ "nombre" : n })

    return None if wiki_doc is None else json.loads(json_util.dumps(wiki_doc))


async def getWikiPorID(id: ObjectId):
    wiki_doc = wikiBD.find_one({ "_id": id })
    
    return None if wiki_doc is None else json.loads(json_util.dumps(wiki_doc))


async def getTodasWikis():
    wikis_doc = wikiBD.find().sort({"nombre":1})
    wikis_json = [json.loads(json_util.dumps(doc)) for doc in wikis_doc]    # collection.find() retrieves documents in BSON format from MongoDB.
                                                                            # json_util.dumps(doc) converts BSON documents, including ObjectId fields, to JSON strings.
                                                                            # json.loads(...) transforms each document back into a Python dictionary, so it’s compatible with FastAPI's JSON response model.
    return wikis_json


async def crearWiki(nombre: str, descripcion: str):
    fecha = datetime.utcnow()
    nuevaWiki = {
        "nombre": nombre,
        "fecha": fecha,
        "descripcion": descripcion
    }
    
    result = wikiBD.insert_one(nuevaWiki)
    # devolvemos la nueva wiki al cliente, incluyendo la ID
    nuevaWiki["_id"] = str(result.inserted_id)
    return nuevaWiki


async def eliminarWiki(wiki_id: ObjectId):
    
    result = wikiBD.delete_one({"_id": wiki_id})

    return result


async def actualizarWiki(wiki_id: ObjectId, nombre: str, descripcion: str):
    result = wikiBD.update_one({"_id": wiki_id},
                                {"$set":
                                 {"nombre": nombre,
                                 "descripcion": descripcion}
                                })
    return result


async def getWikisPorNombre(term: str):
    wikis_doc = wikiBD.find({"nombre": {"$regex": term, "$options": "i"}})
    wikis_json = [json.loads(json_util.dumps(doc)) for doc in wikis_doc]
    
    return wikis_json