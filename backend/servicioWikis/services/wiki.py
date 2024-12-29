from bson import json_util
from bson.objectid import ObjectId
import json
from datetime import datetime


# conexion al servidor MongoDB

import bd
wikiBD = bd.wikiBD

# ejecutar con  cd src -> python -m uvicorn main:api --reload --port 8000

async def getWiki(nombre : str):
    wikiDoc = wikiBD.find_one({ "nombre" : nombre })

    return None if wikiDoc is None else json.loads(json_util.dumps(wikiDoc))


async def getTodasWikis():
    wikisDoc = wikiBD.find().sort({"nombre":1})
    wikisJSON = [json.loads(json_util.dumps(doc)) for doc in wikisDoc]    # collection.find() retrieves documents in BSON format from MongoDB.
                                                                            # json_util.dumps(doc) converts BSON documents, including ObjectId fields, to JSON strings.
                                                                            # json.loads(...) transforms each document back into a Python dictionary, so it’s compatible with FastAPI's JSON response model.
    return wikisJSON

async def getWikiPorID(id: ObjectId):
    wikiDoc = wikiBD.find_one({ "_id": id })
    
    return None if wikiDoc is None else json.loads(json_util.dumps(wikiDoc))


async def getWikisPorFiltros(term: str, minFecha: str, maxFecha: str):
    filtro = {}

    if term is not None:
        filtro["nombre"] = {"$regex": term, "$options": "i"}

    if minFecha is not None or maxFecha is not None:
        try:
            # Intentar analizar como formato simple '%Y-%m-%d'
            minDatetime = datetime.min if minFecha is None else datetime.strptime(minFecha, "%Y-%m-%d")
        except ValueError:
            # Intentar analizar como ISO formato '%Y-%m-%dT%H:%M:%SZ'
            minDatetime = datetime.min if minFecha is None else datetime.strptime(minFecha, "%Y-%m-%dT%H:%M:%SZ")

        try:
            maxDatetime = datetime.max if maxFecha is None else datetime.strptime(maxFecha, "%Y-%m-%d")
        except ValueError:
            maxDatetime = datetime.max if maxFecha is None else datetime.strptime(maxFecha, "%Y-%m-%dT%H:%M:%SZ")

        filtro["fecha"] = {
            "$gte": minDatetime,
            "$lte": maxDatetime
        }

    wikisDoc = wikiBD.find(filtro)
    wikisJSON = [json.loads(json_util.dumps(doc)) for doc in wikisDoc]
    
    return wikisJSON


async def crearWiki(nombre: str, descripcion: str, portada : str, cabecera : str):
    fecha = datetime.utcnow()
    nuevaWiki = {
        "nombre": nombre,
        "fecha": fecha,
        "descripcion": descripcion,
        "portada": portada,
        "cabecera" : cabecera
    }
    
    result = wikiBD.insert_one(nuevaWiki)
    # devolvemos la nueva wiki al cliente, incluyendo la ID
    nuevaWiki["_id"] = str(result.inserted_id)
    return nuevaWiki


async def eliminarWiki(wikiID: ObjectId):
    
    result = wikiBD.delete_one({"_id": wikiID})

    return result


async def actualizarWiki(wikiID: ObjectId, nombre: str, descripcion: str, portada : str, cabecera : str):
    result = wikiBD.update_one({"_id": wikiID},
                                {"$set":
                                 {"nombre": nombre,
                                 "descripcion": descripcion,
                                 "portada": portada,
                                 "cabecera": cabecera}
                                })
    return result