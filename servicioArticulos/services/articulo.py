from typing import Any
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime

from bd import BD_articulo, BD_usuario

async def getArticulo(t: str):
    articulo_doc = BD_articulo.find_one({ "titulo" : t })    
    articulo_json = json.loads(json_util.dumps(articulo_doc))

    return articulo_json


async def getTodosArticulos(wiki_id: ObjectId):
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

async def buscarUsuarioOrdenado(usuario: str, wiki: ObjectId):
    usu= BD_usuario.find_one({"nombre": usuario})
    usu_json = json.loads(json_util.dumps(usu))
    usu_dict = usu_json["_id"]
    usu_id = usu_dict["$oid"]
    usuId = ObjectId(usu_id)

    articulos_doc = BD_articulo.find({"creador": usuId,
                                      "wiki": wiki}).sort("fecha", -1)
    articulos_json = [json.loads(json_util.dumps(doc)) for doc in articulos_doc]
    
    return articulos_json
