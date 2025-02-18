from services import articulo as articuloAPI
from services import imagenes
from services import mapa as mapaAPI
from services import traducir as traducirAPI

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
async def getArticulos(
    term: str = Query(None, min_length=1),
    usuario: str = Query(None, min_length=1),
    wiki: str = Query(None, min_length=1),
    minFecha: str = Query(None, min_length=1),
    maxFecha: str = Query(None, min_length=1),
    idioma: str = Query(None, min_length=1)
    ):
    hayFiltros = term is not None or wiki is not None or minFecha is not None or maxFecha is not None or usuario is not None or idioma is not None

    if wiki is not None:
        wikiObjID = getObjID(wiki)
    else:
        wikiObjID = None

    if hayFiltros:
         listaArticulos = await articuloAPI.getArticulosPorFiltros(
            wikiID=wikiObjID,
            term=term,
            minFecha=minFecha,
            maxFecha=maxFecha,
            creador=usuario,
            idioma=idioma
        )
    else:
        listaArticulos = await articuloAPI.getTodosArticulos()

    return listaArticulos

@api.get(path + "/wikis/{nombre}/idiomas")
async def idiomasWiki(wiki: str = Query(...)):
    if wiki is not None:
        wikiObjID = getObjID(wiki)
    else:
        wikiObjID = None
    idiomas = await articuloAPI.getIdiomas(wikiObjID)

    return idiomas


@api.get(path + "/wikis/{nombre}/articulos/idioma")
async def idiomasArticulo(wiki: str = Query(None, min_length=1), idioma : str = Query(None, min_length=1)):
    if wiki is not None:
        wikiObjID = getObjID(wiki)
    else:
        wikiObjID = None
    listaArticulos = await articuloAPI.getArticulosPorIdioma(wikiObjID, idioma)

    return listaArticulos


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
    idioma = data.get("idioma")
    if isinstance(creador, dict) and "$oid" in creador:
        creador = ObjectId(creador["$oid"])  # Convert the string inside "$oid" to ObjectId

    # If 'creador' is already an ObjectId string or directly an ObjectId
    elif isinstance(creador, str):
        creador = ObjectId(creador)

    articuloJSON = await articuloAPI.getArticulo(wiki, titulo)
   
    return await articuloAPI.crearArticulo(titulo, wiki, contenido, creador, idioma) if articuloJSON is None else "Ya existe un articulo con ese nombre"


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
    idioma = data.get("idioma")
    if isinstance(creador, dict) and "$oid" in creador:
        creador = ObjectId(creador["$oid"])  # Convert the string inside "$oid" to ObjectId

    # If 'creador' is already an ObjectId string or directly an ObjectId
    elif isinstance(creador, str):
        creador = ObjectId(creador)

    result = await articuloAPI.actualizarArticulo(titulo, wiki, contenido, creador, idioma)

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

@api.get(path + "/wikis/{nombre}/articulos/{titulo}/versiones")
async def todasVersiones(titulo : str, idioma : str = Query(...)):
    articulo_json = await articuloAPI.versionesAnteriores(titulo, idioma)

    if articulo_json is None:
        raise HTTPException(status_code=404, detail="El artículo no tiene más versiones")
    return articulo_json

@api.put(path + "/wikis/{nombre}/articulos/{titulo}/cambiarVersion")
async def cambiarVersion(idActual : str = Query(...), idVolver : str = Query(...)):
    actualID = getObjID(idActual)
    volverID = getObjID(idVolver)

    result = await articuloAPI.cambiarVersion(actualID, volverID)

    return result

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
   
    return "Ya existe una imagen con ese nombre" if enlace is None else f"Subido con éxito a {enlace}"

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
   
    return await mapaAPI.crearMapa(latitud, longitud, nombreUbicacion, articulo)

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
    artObjID = getObjID(id)
    result = await mapaAPI.eliminarMapa(artObjID)
        

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail=f"Versión del artículo no encontrada")

    return "Mapa eliminado con éxito"

# TRADUCIR UN ARTÍCULO
@api.put(path + "/wikis/{nombre}/articulos/{titulo}/traducir")
async def traducirArticulo(nombre: str, titulo: str, idioma: str = Query(...)):
    wikiObjID = getObjID(nombre)
    articulo = await articuloAPI.getArticulo(wikiObjID, titulo)
    
    wiki = wikiObjID
    contenido = articulo.get("contenido")
    contenidoTraducido = traducirAPI.traducirTexto(contenido, idioma)
    tituloTraducido = traducirAPI.traducirTexto(titulo, idioma)
    creador = articulo.get("creador")
    if isinstance(creador, dict) and "$oid" in creador:
        creador = ObjectId(creador["$oid"])  # Convert the string inside "$oid" to ObjectId

    # If 'creador' is already an ObjectId string or directly an ObjectId
    elif isinstance(creador, str):
        creador = ObjectId(creador)

    result = await articuloAPI.actualizarArticulo(tituloTraducido, wiki, contenidoTraducido, creador, idioma)

    return result

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