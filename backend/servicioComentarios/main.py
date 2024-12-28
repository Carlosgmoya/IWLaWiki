#ejecutar de manera local -> python -m uvicorn main:api --reload --port 8003
from fastapi import FastAPI, HTTPException, Query

from bson.objectid import ObjectId
from typing import List
from fastapi.middleware.cors import CORSMiddleware

from models import Comentario
from bd import comentarioBD

# prefijo para todas las URLs
path = "/api/v1"

api = FastAPI()

api.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@api.get(path + "/comentarios", response_model=List[Comentario])
def getComentarios():
    """Devuelve todos los comentarios."""
    comentarios = list(comentarioBD.find())
    return [Comentario(**comentario) for comentario in comentarios]

@api.get(path + "/comentarios/articulo/{articuloId}", response_model=List[Comentario])
def getComentariosPorArticulo(articuloId: str):
    """Devuelve los comentarios de un artículo dado su ID."""
    comentarios = list(comentarioBD.find({"articulo_id": ObjectId(articuloId)}))
    if not comentarios:
        raise HTTPException(status_code=404, detail="No se encontraron comentarios para este artículo.")
    return [Comentario(**comentario) for comentario in comentarios]

@api.get(path + "/comentarios/usuario/{usuario}", response_model=List[Comentario])
def getComentariosPorUsuario(usuario: str):
    """Devuelve los comentarios de un usuario dado su nombre."""
    comentarios = list(comentarioBD.find({"usuario": usuario}))
    if not comentarios:
        raise HTTPException(status_code=404, detail="No se encontraron comentarios para este usuario.")
    return [Comentario(**comentario) for comentario in comentarios]


@api.get(path + "/comentarios/articulo/{articuloId}/usuario/{usuario}", response_model=List[Comentario])
def getComentariosPorArticuloYUsuario(articuloId: str, usuario: str):
    """Devuelve los comentarios de un usuario en un artículo."""
    comentarios = list(comentarioBD.find({
        "usuario": usuario,
        "articulo_id": ObjectId(articuloId)
    }))
    if not comentarios:
        raise HTTPException(status_code=404, detail="No se encontraron comentarios para este usuario en este artículo.")
    return [Comentario(**comentario) for comentario in comentarios]


@api.post(path + "/comentarios", response_model=Comentario)
def crearComentario(comentario: Comentario):
    """Crea un nuevo comentario."""
    comentario_dict = comentario.dict(by_alias=True)
    resultado = comentarioBD.insert_one(comentario_dict)
    comentario_dict["_id"] = resultado.inserted_id
    return Comentario(**comentario_dict)

@api.put(path + "/comentarios/{comentarioId}", response_model=Comentario)
def actualizarComentario(comentarioId: str, comentario: Comentario):
    """Actualiza un comentario dado su ID."""
    comentarioDict = comentario.dict(by_alias=True, exclude={"id"})
    resultado = comentarioBD.update_one({"_id": ObjectId(comentarioId)}, {"$set": comentarioDict})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Comentario no encontrado.")
    comentarioDict["_id"] = ObjectId(comentarioId)
    return Comentario(**comentarioDict)

@api.delete(path + "/comentarios/{comentarioId}", response_model=dict)
def eliminarComentario(comentarioId: str):
    """Elimina un comentario dado su ID."""
    resultado = comentarioBD.delete_one({"_id": ObjectId(comentarioId)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Comentario no encontrado.")
    return {"message": "Comentario eliminado correctamente."}