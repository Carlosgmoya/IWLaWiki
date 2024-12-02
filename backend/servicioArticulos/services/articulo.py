from typing import Any
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json
from datetime import datetime

from bd import articuloBD, usuarioBD

async def getArticulo(wikiID: ObjectId, t: str):
    articulo_doc = articuloBD.find_one({ "titulo" : t,
                                         "wiki": wikiID,
                                          "ultimoModificado": True })    
    articulo_json = json.loads(json_util.dumps(articulo_doc))

    return articulo_json


async def getTodosArticulos(wikiID: ObjectId):
    articulosDoc = articuloBD.find({"wiki": wikiID,"ultimoModificado": True})
    articulosJSON = json.loads(json_util.dumps(articulosDoc))

    return articulosJSON


async def getArticulosPorTitulo(wikiID: ObjectId, term: str):
    articulosDoc = articuloBD.find({"titulo": {"$regex": term, "$options": "i"},
                                      "wiki": wikiID,"ultimoModificado": True})
    articulosJSON = [json.loads(json_util.dumps(doc)) for doc in articulosDoc]
    
    return articulosJSON


async def getArticulosPorTituloYContenido(wikiID: ObjectId, term: str):
    terms = term.split()

    regex_patterns = [{"titulo": {"$regex": t, "$options": "i"}} for t in terms] + \
                 [{"contenido": {"$regex": t, "$options": "i"}} for t in terms]
    
    articulosDoc = articuloBD.find({
        "$and": [
            {"$or": regex_patterns},
            {"wiki": wikiID},
            {"ultimoModificado": True}
        ]
    })

    articulosJSON = [json.loads(json_util.dumps(doc)) for doc in articulosDoc]

    return articulosJSON


async def buscarVersionPorFecha(titulo: str, fecha: datetime):
    articulo_doc = articuloBD.find_one({"titulo" : titulo, "fecha" : fecha})
    articulo_json = json.loads(json_util.dumps(articulo_doc))
    return articulo_json


async def crearArticulo(titulo: str, wiki: ObjectId, contenido: str, creador: ObjectId):
    fecha = datetime.utcnow()
    nuevoArticulo = {
        "titulo": titulo,
        "wiki": wiki,
        "fecha": fecha,
        "ultimoModificado": True,
        "contenido": contenido,
        "creador": creador
    }
    result = articuloBD.insert_one(nuevoArticulo)
    nuevoArticulo["_id"] = str(result.inserted_id)
    nuevoArticulo["wiki"] = str(wiki)
    nuevoArticulo["creador"] = str(creador)
    
    return nuevoArticulo


async def actualizarArticulo(titulo: str, wiki: ObjectId, contenido: str, creador: ObjectId):
    fecha = datetime.utcnow()
    nuevaVersion = {
        "titulo": titulo,
        "wiki": wiki,
        "fecha": fecha,
        "ultimoModificado": True,
        "contenido": contenido,
        "creador": creador
    }

    #Actualiza el estado UltimoModificado de la version anterior a false
    articuloBD.update_many(
        {"titulo": titulo, "wiki": wiki},
        {"$set": {"ultimoModificado": False}}
    )

    result = articuloBD.insert_one(nuevaVersion)
    nuevaVersion["_id"] = str(result.inserted_id)
    nuevaVersion["wiki"] = str(wiki)
    nuevaVersion["creador"] = str(creador)

    return nuevaVersion


async def eliminarVersionArticulo(articulo_id: ObjectId):
    result = articuloBD.delete_one({"_id": articulo_id})
    return result

async def eliminarTodasVersionesArticulo(titulo: str):
    result = articuloBD.delete_many({"titulo": titulo})
    return result

#Modificar un articulo seria crear uno nuevo

async def getArticulosPorUsuarioOrdenadoPorFecha(wiki: ObjectId, usuario: str):
    # ELIMINAR EL ACCESO A usuarioBD cuando se implemente el microservicio usuario
    usu= usuarioBD.find_one({"nombre": usuario})
    usu_json = json.loads(json_util.dumps(usu))
    usu_dict = usu_json["_id"]
    usu_id = usu_dict["$oid"]
    usuId = ObjectId(usu_id)

    articulosDoc = articuloBD.find({"creador": usuId,
                                      "wiki": wiki}).sort("fecha", -1)
    articulosJSON = [json.loads(json_util.dumps(doc)) for doc in articulosDoc]
    
    return articulosJSON




