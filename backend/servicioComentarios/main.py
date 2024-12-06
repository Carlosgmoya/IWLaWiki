#ejecutar de manera local -> python -m uvicorn main:api --reload --port 8003
from fastapi import FastAPI, HTTPException, Query
from bson.objectid import ObjectId
from typing import List
from datetime import datetime

from models import Comentario
from bd import comentarioBD

# prefijo para todas las URLs
path = "/api/v1"

api = FastAPI()

@api.get(path + "/insertComentarios")
async def crear_comentario():
    # Crear comentarios de ejemplo
    comentarios = [
        Comentario(
            fecha=datetime.utcnow(),
            usuario_id=ObjectId("651fcdfdf45c1f9bfed57032"),
            articulo_id=ObjectId("651fcdfdf45c1f9bfed57033"),
            contenido="Este es un comentario de ejemplo 1."
        ),
        Comentario(
            fecha=datetime.utcnow(),
            usuario_id=ObjectId("651fcdfdf45c1f9bfed57034"),
            articulo_id=ObjectId("651fcdfdf45c1f9bfed57035"),
            contenido="Este es un comentario de ejemplo 2."
        ),
        Comentario(
            fecha=datetime.utcnow(),
            usuario_id=ObjectId("651fcdfdf45c1f9bfed57036"),
            articulo_id=ObjectId("651fcdfdf45c1f9bfed57037"),
            contenido="Este es un comentario de ejemplo 3."
        ),
    ]

    # Insertar en la base de datos
    resultado = comentarioBD.insert_many([comentario.dict(by_alias=True) for comentario in comentarios])
    return f"Comentarios insertados con IDs: {resultado.inserted_ids}"


@api.get(path + "/comentarios", response_model=List[Comentario])
def get_comentarios():
    """Devuelve todos los comentarios."""
    comentarios = list(comentarioBD.find())
    return [Comentario(**comentario) for comentario in comentarios]

@api.get(path + "/comentarios/articulo/{articulo_id}", response_model=List[Comentario])
def get_comentarios_por_articulo(articulo_id: str):
    """Devuelve los comentarios de un artículo dado su ID."""
    comentarios = list(comentarioBD.find({"articulo_id": ObjectId(articulo_id)}))
    if not comentarios:
        raise HTTPException(status_code=404, detail="No se encontraron comentarios para este artículo.")
    return [Comentario(**comentario) for comentario in comentarios]

@api.get(path + "/comentarios/usuario/{usuario_id}", response_model=List[Comentario])
def get_comentarios_por_usuario(usuario_id: str):
    """Devuelve los comentarios de un usuario dado su ID."""
    comentarios = list(comentarioBD.find({"usuario_id": ObjectId(usuario_id)}))
    if not comentarios:
        raise HTTPException(status_code=404, detail="No se encontraron comentarios para este usuario.")
    return [Comentario(**comentario) for comentario in comentarios]

@api.post(path + "/comentarios", response_model=Comentario)
def crear_comentario(comentario: Comentario):
    """Crea un nuevo comentario."""
    comentario_dict = comentario.dict(by_alias=True)
    resultado = comentarioBD.insert_one(comentario_dict)
    comentario_dict["_id"] = resultado.inserted_id
    return Comentario(**comentario_dict)

@api.put(path + "/comentarios/{comentario_id}", response_model=Comentario)
def actualizar_comentario(comentario_id: str, comentario: Comentario):
    """Actualiza un comentario dado su ID."""
    comentario_dict = comentario.dict(by_alias=True, exclude={"id"})
    resultado = comentarioBD.update_one({"_id": ObjectId(comentario_id)}, {"$set": comentario_dict})
    if resultado.matched_count == 0:
        raise HTTPException(status_code=404, detail="Comentario no encontrado.")
    comentario_dict["_id"] = ObjectId(comentario_id)
    return Comentario(**comentario_dict)

@api.delete(path + "/comentarios/{comentario_id}", response_model=dict)
def eliminar_comentario(comentario_id: str):
    """Elimina un comentario dado su ID."""
    resultado = comentarioBD.delete_one({"_id": ObjectId(comentario_id)})
    if resultado.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Comentario no encontrado.")
    return {"message": "Comentario eliminado correctamente."}