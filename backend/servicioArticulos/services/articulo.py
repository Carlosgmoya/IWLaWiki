from bson import json_util
from bson.objectid import ObjectId
import json
from datetime import datetime

from bd import articuloBD, usuarioBD

async def getArticulo(wikiID: ObjectId, t: str):
    articuloDoc = articuloBD.find_one({ "titulo" : t,
                                         "wiki": wikiID,
                                          "ultimoModificado": True })    
    articuloJson = json.loads(json_util.dumps(articuloDoc))

    return articuloJson


async def getTodosArticulos(wikiID: ObjectId):
    articulosDoc = articuloBD.find({"wiki": wikiID,"ultimoModificado": True})
    articulosJSON = json.loads(json_util.dumps(articulosDoc))

    return articulosJSON


#async def getArticulosPorTitulo(wikiID: ObjectId, term: str):
#    articulosDoc = articuloBD.find({"titulo": {"$regex": term, "$options": "i"},
#                                      "wiki": wikiID,"ultimoModificado": True})
#    articulosJSON = [json.loads(json_util.dumps(doc)) for doc in articulosDoc]
#    
#    return articulosJSON


#async def getArticulosPorTituloYContenido(wikiID: ObjectId, term: str):
#    terms = term.split()
#
#    regex_patterns = [{"titulo": {"$regex": t, "$options": "i"}} for t in terms] + \
#                 [{"contenido": {"$regex": t, "$options": "i"}} for t in terms]
#    
#    articulosDoc = articuloBD.find({
#        "$and": [
#            {"$or": regex_patterns},
#            {"wiki": wikiID},
#            {"ultimoModificado": True}
#        ]
#    })
#
#    articulosJSON = [json.loads(json_util.dumps(doc)) for doc in articulosDoc]
#
#    return articulosJSON


async def getArticulosPorFiltros(wikiID: ObjectId, term: str, minFecha: str, maxFecha: str, creador: str, idioma: str):
    filtro = {"$and": [{"ultimoModificado": True}]}

    if wikiID is not None:
        filtro["$and"].append({"wiki": wikiID})

    if term is not None:
        terms = term.split()

        regex_patterns = [{"titulo": {"$regex": t, "$options": "i"}} for t in terms] + \
            [{"contenido": {"$regex": t, "$options": "i"}} for t in terms]
    
        filtro["$and"].append({"$or": regex_patterns})

    if minFecha is not None or maxFecha is not None:
        try:
            minDatetime = datetime.min if minFecha is None else datetime.strptime(minFecha, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            minDatetime = datetime.min if minFecha is None else datetime.strptime(minFecha, "%Y-%m-%dT%H:%M:%SZ")

        try:
            maxDatetime = datetime.max if maxFecha is None else datetime.strptime(maxFecha, "%Y-%m-%dT%H:%M:%S.%fZ")
        except ValueError:
            maxDatetime = datetime.max if maxFecha is None else datetime.strptime(maxFecha, "%Y-%m-%dT%H:%M:%SZ")
        
        filtro["$and"].append({
            "fecha": {
                "$gte": minDatetime,
                "$lte": maxDatetime
            }
        })

    if creador is not None:
        usuario = usuarioBD.find_one({"nombre": creador})
        usuarioJson = json.loads(json_util.dumps(usuario))
        usuarioId = ObjectId(usuarioJson["_id"]["$oid"])

        filtro["$and"].append({"creador": usuarioId})
    
    if idioma is not None:
        filtro["$and"].append({"idioma": idioma})
    
    articulosDoc = articuloBD.find(filtro)

    articulosJSON = [json.loads(json_util.dumps(doc)) for doc in articulosDoc]

    return articulosJSON


async def buscarVersionPorFecha(titulo: str, fecha: datetime):
    articulo_doc = articuloBD.find_one({"titulo" : titulo, "fecha" : fecha})
    articulo_json = json.loads(json_util.dumps(articulo_doc))
    return articulo_json


async def crearArticulo(titulo: str, wiki: ObjectId, contenido: str, creador: ObjectId, idioma : str):
    fecha = datetime.utcnow()
    nuevoArticulo = {
        "titulo": titulo,
        "wiki": wiki,
        "fecha": fecha,
        "ultimoModificado": True,
        "contenido": contenido,
        "creador": creador,
        "fechaCreacion": fecha,
        "idioma": idioma
    }
    result = articuloBD.insert_one(nuevoArticulo)
    nuevoArticulo["_id"] = str(result.inserted_id)
    nuevoArticulo["wiki"] = str(wiki)
    nuevoArticulo["creador"] = str(creador)
    
    return nuevoArticulo


async def actualizarArticulo(titulo: str, wiki: ObjectId, contenido: str, creador: ObjectId, idioma : str):
    fecha = datetime.utcnow()
    primerArticulo = articuloBD.find_one({"titulo": titulo}, sort=[("fechaCreacion", 1)])
    if primerArticulo:
        fechaCreacion = primerArticulo.get("fechaCreacion")
    else:
        fechaCreacion = fecha
    nuevaVersion = {
        "titulo": titulo,
        "wiki": wiki,
        "fecha": fecha,
        "ultimoModificado": True,
        "contenido": contenido,
        "creador": creador,
        "fechaCreacion": fechaCreacion,
        "idioma" : idioma
    }

    #Actualiza el estado UltimoModificado de la version anterior a false
    articuloBD.update_many(
        {"titulo": titulo, "wiki": wiki, "idioma": idioma, "ultimoModificado": True},
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

async def versionesAnteriores(titulo : str):
    articulosDoc = articuloBD.find({"titulo": titulo,"ultimoModificado": False})
    articulosJSON = json.loads(json_util.dumps(articulosDoc))

    return articulosJSON

async def cambiarVersion(idActual : ObjectId, idVolver : ObjectId):
    result1 = articuloBD.update_one(
        {"_id" :idActual},
        {"$set": {"ultimoModificado": False}}
    )
    result2 = articuloBD.update_one(
        {"_id" :idVolver},
        {"$set": {"ultimoModificado": True}}
    )

    if result1.matched_count == 0:
        return "Error al encontrar el articulo actual"
    elif result2.matched_count == 0:
        return "Error al encontrar la version anterior del articulo"
    else :
        return "Articulo cambiado de version" 


