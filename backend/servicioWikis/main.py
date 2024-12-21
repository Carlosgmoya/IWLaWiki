from services import wiki as wikiAPI
from services import imagenes
import os
from pathlib import Path
import shutil

from fastapi import FastAPI, Request, HTTPException, Query, UploadFile, File, Form
from bson.objectid import ObjectId


api = FastAPI()

# prefijo para todas las URLs
path = "/api/v1"

# Desde el directorio de este archivo: 2 maneras de ejecutar el modulo:
#   -ejecutar de manera local -> python -m uvicorn main:api --reload --port 8001
#   -ejecutar el contenedor Docker -> docker run -p 8001:8001 fu17alex/modulowiki:v1.0


# PAGINA PRINCIPAL: DEVUELVE TODAS LAS WIKIS O DEVUELVE LAS WIKIS QUE CUMPLEN UNOS CRITERIOS
@api.get(path + "/wikis")
async def getWikis(term: str = Query(None, min_length=1)):
    return await wikiAPI.getTodasWikis() if term is None else await wikiAPI.getWikisPorNombre(term)


# PAGINA WIKI
@api.get(path + "/wikis/{nombre}")
async def getWiki(nombre: str):
    wikiJSON = await wikiAPI.getWiki(nombre)
    if wikiJSON is None:
        raise HTTPException(status_code=404, detail="Wiki no encontrado")
    
    return wikiJSON
    
    
# CREAR WIKI
@api.post(path + "/wikis")
async def crearWiki(nombre : str = Form(...), descripcion : str = Form(...) , archivoP : UploadFile = File(...), archivoC : UploadFile = File(...)):
    carpetaDestino = Path("imagenesTemporales")
    carpetaDestino.mkdir(parents=True, exist_ok=True)
    rutaLocalP = carpetaDestino / archivoP.filename
    with rutaLocalP.open("wb") as buffer:
        shutil.copyfileobj(archivoP.file, buffer)

    if rutaLocalP:  # Si el usuario seleccionó un archivo
        rutaRemotaP = f"/{archivoP.filename}"  # Asignar un nombre de archivo en Dropbox
        imagenes.subirImagenDropbox(rutaLocalP, rutaRemotaP)
        portada = imagenes.obtenerEnlaceImagen(rutaRemotaP)
    else:
        print("No se seleccionó ningún archivo.")

    rutaLocalC = carpetaDestino / archivoC.filename
    with rutaLocalC.open("wb") as buffer:
        shutil.copyfileobj(archivoC.file, buffer)

    if rutaLocalC:  # Si el usuario seleccionó un archivo
        rutaRemotaC = f"/{archivoC.filename}"  # Asignar un nombre de archivo en Dropbox
        imagenes.subirImagenDropbox(rutaLocalC, rutaRemotaC)
        cabecera = imagenes.obtenerEnlaceImagen(rutaRemotaC)
    else:
        print("No se seleccionó ningún archivo.")
    wikiJSON = await wikiAPI.getWiki(nombre)

    os.remove(rutaLocalP)
    os.remove(rutaLocalC)
    return await wikiAPI.crearWiki(nombre, descripcion, portada, cabecera) if wikiJSON is None else "Ya existe una wiki con ese nombre"


# ACTUALIZAR WIKI
@api.put(path + "/wikis/{wikiID}")
async def actualizarWiki(request: Request, wikiID: str):
    try:
        ObjID = ObjectId(wikiID)
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid ObjectId format")
    
    data = await request.json()
    nombre = data.get("nombre")
    descripcion = data.get("descripcion")
    portada = data.get("portada")
    cabecera = data.get("cabecera")
    
    result = await wikiAPI.actualizarWiki(ObjID, nombre, descripcion, portada, cabecera)
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Wiki no encontrada")
    if result.modified_count == 0:
        return "No se realizaron cambios"
    
    return "Wiki actualizada con éxito"


# ELIMINAR WIKI
@api.delete(path + "/wikis/{wikiID}")
async def eliminarWiki(wikiID: str):
    try:
        obj_id = ObjectId(wikiID)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID inválido")
    
    result = await wikiAPI.eliminarWiki(obj_id)
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Wiki no encontrada")

    return "Wiki eliminada con éxito"