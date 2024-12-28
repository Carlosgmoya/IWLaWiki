from bson import json_util
from bson.objectid import ObjectId
from fastapi import HTTPException
import json

from bd import mapaBD

async def getMapa(artID: ObjectId):
    mapasDoc = mapaBD.find_one({"articulo": artID})  
    if not mapasDoc:
        raise HTTPException(status_code=404, detail="Mapa no encontrado")
    mapasJSON = json.loads(json_util.dumps(mapasDoc))

    return mapasJSON

async def crearMapa(latitud: float, longitud: float, nombreUbicacion: str, articulo: ObjectId):
    nuevoMapa = {
        "latitud": latitud,
        "longitud": longitud,
        "nombreUbicacion": nombreUbicacion,
        "articulo": articulo
    }
    result = mapaBD.insert_one(nuevoMapa)
    nuevoMapa["_id"] = str(result.inserted_id)
    nuevoMapa["articulo"] = str(articulo)
    
    return nuevoMapa

async def actualizarMapa(mapaId: ObjectId, latitud: float, longitud: float, nombreUbicacion: str, articulo: ObjectId):
    
    result = mapaBD.update_one({"_id": mapaId},
                                {"$set": {  # Operador $set para actualizar campos específicos
                                    "latitud": latitud,
                                    "longitud": longitud,
                                    "nombreUbicacion": nombreUbicacion,
                                    "articulo": articulo
                                }})
    return {
        "matched_count": result.matched_count,  # Número de documentos encontrados
        "modified_count": result.modified_count,  # Número de documentos modificados
        "acknowledged": result.acknowledged  # Si la operación fue reconocida por el servidor
    }

async def eliminarMapa(artId: ObjectId):
    result = mapaBD.delete_one({"articulo": artId})
    return result