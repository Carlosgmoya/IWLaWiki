from services import articulo as articuloAPI
from services import imagenes
from services import mapa as mapaAPI

from fastapi import FastAPI, Request, HTTPException, Query, UploadFile, File

from bson.objectid import ObjectId
import json
from markdown import markdown
import os
from pathlib import Path
import shutil

api = FastAPI()

# prefijo para todas las URLs
path = "/api/v1" 

api = FastAPI()

#   -ejecutar de manera local -> python -m uvicorn main:api --reload --port 8002


def getObjID(id: str):
    try:
        objID = ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID de wiki inválido")

    return objID


# GET ARTICULOS DE UNA WIKI
@api.get(path + "/wikis/{nombre}/articulos")
async def getArticulos(terminoDeBusqueda: str | None = None, usuario: str | None = None, wiki: str = Query(...)):
    wikiObjID = getObjID(wiki)

    if terminoDeBusqueda is not None:
        articulosJSON = await articuloAPI.getArticulosPorTituloYContenido(wikiObjID, terminoDeBusqueda)
    elif usuario is not None:
        articulosJSON = await articuloAPI.getArticulosPorUsuarioOrdenadoPorFecha(wikiObjID, usuario) # se accede a la base de datos de usuario desde aqui porque aun no se ha implementado el modulo "usuario"
    else:
        articulosJSON = await articuloAPI.getTodosArticulos(wikiObjID)

    return articulosJSON


# GET ARTICULO
@api.get(path + "/wikis/{nombre}/articulos/{titulo}")
async def getArticulo(titulo : str, wiki: str = Query(...)):
    wikiObjID = getObjID(wiki)
    
    articulo_json = await articuloAPI.getArticulo(wikiObjID, titulo)

    if articulo_json is None:
        raise HTTPException(status_code=404, detail="Artículo no encontrado")
     # Formatear el contenido de cada artículo
    articulo_json["contenido_html"] = convertirAHtml( articulo_json["contenido"])
    #articulo_json["contenido"] = formatearContenido(articulo_json["contenido"])
    
    return articulo_json


# CREAR ARTICULO
@api.post(path + "/wikis/{nombre}/articulos")
async def crearArticulo(request: Request, wiki: str = Query(...)):
    wikiObjID = getObjID(wiki)
    
    try:
        data = await request.json()
    except Exception as e:
        data = {}

    if not data:
        raise HTTPException(status_code=400, detail="Parametros de request vacío")
    
    titulo = data.get("titulo")
    wiki = wikiObjID
    contenido = data.get("contenido")
    creador = data.get("creador")
    if isinstance(creador, dict) and "$oid" in creador:
        creador = ObjectId(creador["$oid"])  # Convert the string inside "$oid" to ObjectId

    # If 'creador' is already an ObjectId string or directly an ObjectId
    elif isinstance(creador, str):
        creador = ObjectId(creador)

    articuloJSON = await articuloAPI.getArticulo(wiki, titulo)
   
    return await articuloAPI.crearArticulo(titulo, wiki, contenido, creador) if articuloJSON is None else "Ya existe un articulo con ese nombre"


# ACTUALIZAR UN ARTÍCULO
@api.put(path + "/wikis/{nombre}/articulos/{titulo}")
async def actualizarArticulo(request: Request, titulo: str, wiki: str = Query(...)):
    wikiObjID = getObjID(wiki)

    try:
        data = await request.json()
    except Exception as e:
        data = {}

    if not data:
        raise HTTPException(status_code=400, detail="Parametros de request vacío")
    
    wiki = wikiObjID
    contenido = data.get("contenido")
    creador = data.get("creador")
    if isinstance(creador, dict) and "$oid" in creador:
        creador = ObjectId(creador["$oid"])  # Convert the string inside "$oid" to ObjectId

    # If 'creador' is already an ObjectId string or directly an ObjectId
    elif isinstance(creador, str):
        creador = ObjectId(creador)

    result = await articuloAPI.actualizarArticulo(titulo, wiki, contenido, creador)

    return result

# BORRAR UNA TODAS LAS VERSIONES DEL ARTÍCULO O SOLO UNA VERSION SI SE PASA ID
@api.delete(path + "/wikis/{nombre}/articulos/{titulo}")
async def eliminarArticulo(titulo: str, id: str = Query(None, min_length=1)):
    if id is None:
        result = await articuloAPI.eliminarTodasVersionesArticulo(titulo)
    else:
        wikiObjID = getObjID(id)
        result = await articuloAPI.eliminarVersionArticulo(wikiObjID)
        

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Versión del artículo no encontrada")

    return "Artículo eliminado con éxito"

# SUBIR ARCHIVOS A DROPBOX
@api.post(path + "/subirImagen")
async def subirImagen(archivo : UploadFile = File(...)):
    #rutaLocal = "C:/Users/cgmoy/Desktop/prueba.png"
    carpeta_destino = Path("imagenes_temporales")
    carpeta_destino.mkdir(parents=True, exist_ok=True)
    rutaLocal = carpeta_destino / archivo.filename
    with rutaLocal.open("wb") as buffer:
        shutil.copyfileobj(archivo.file, buffer)

    if rutaLocal:  # Si el usuario seleccionó un archivo
        rutaRemota = f"/{archivo.filename}"  # Asignar un nombre de archivo en Dropbox
        imagenes.subirImagenDropbox(rutaLocal, rutaRemota)
        enlace = imagenes.obtenerEnlaceImagen(rutaRemota)
    else:
        print("No se seleccionó ningún archivo.")
    os.remove(rutaLocal)
   
    return "Ya existe una imagen con ese nombre" if enlace is None else f"Subido satisfactoria mente a {enlace}"

# GET MAPAS DE UN ARTICULO
@api.get(path + "/wikis/{nombre}/articulos/{titulo}/mapa")
async def getMapas(art: str = Query(...)):
    artObjID = getObjID(art)

    mapasJSON = await mapaAPI.getMapa(artObjID)

    return mapasJSON

# CREAR MAPA
@api.post(path + "/wikis/{nombre}/articulos/{titulo}/mapas")
async def crearMapa(request: Request, art: str = Query(...)):
    artObjID = getObjID(art)
    
    try:
        data = await request.json()
    except Exception as e:
        data = {}

    if not data:
        raise HTTPException(status_code=400, detail="Parametros de request vacío")
    
    latitud = data.get("latitud")
    longitud = data.get("longitud")
    nombreUbicacion = data.get("nombreUbicacion")
    articulo = artObjID

    mapaJSON = await mapaAPI.getMapa(art)
   
    return await mapaAPI.crearMapa(latitud, longitud, nombreUbicacion, articulo) if mapaJSON is None else "Ya existe un articulo con ese nombre"

# ACTUALIZAR MAPA
@api.put(path + "/wikis/{nombre}/articulos/{titulo}/mapas")
async def actualizarMapa(request: Request,mapa: str, art: str = Query(...)):
    artObjID = getObjID(art)
    mapaObjID = getObjID(mapa)
    
    try:
        data = await request.json()
    except Exception as e:
        data = {}

    if not data:
        raise HTTPException(status_code=400, detail="Parametros de request vacío")
    
    mapa = mapaObjID
    latitud = data.get("latitud")
    longitud = data.get("longitud")
    nombreUbicacion = data.get("nombreUbicacion")
    articulo = artObjID
   
    result = await mapaAPI.actualizarMapa(mapaObjID, latitud, longitud, nombreUbicacion, articulo)
    return result

# BORRAR UN MAPA
@api.delete(path + "/wikis/{nombre}/articulos/{titulo}/borrarMapa")
async def eliminarMapa(id: str = Query(None, min_length=1)):
    mapaObjID = getObjID(id)
    result = await mapaAPI.eliminarMapa(mapaObjID)
        

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Versión del artículo no encontrada")

    return "Mapa eliminado con éxito"

########## Metodos Complementarios ############


def getWikiObjID(wikiJSON: json):
    wikiDict = wikiJSON["_id"]
    wikiID = wikiDict["$oid"]

    try:
        objID = ObjectId(wikiID)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID de wiki inválido")
    
    return objID


def convertirAHtml(contenido_md: str) -> str:
    return markdown(contenido_md)

# def formatearContenido(contenido):
#     patron_titulo = r"==\s*(.+?)\s*=="
#     partes = re.split(patron_titulo, contenido)
    
#     contenido_formateado = []
#     for i in range(1, len(partes), 2):
#         subtitulo = partes[i].strip()
#         cuerpo = partes[i + 1].strip()
#         contenido_formateado.append({
#             "subtitulo": subtitulo,
#             "cuerpo": cuerpo
#         })
#     return contenido_formateado