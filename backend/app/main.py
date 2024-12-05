from fastapi import FastAPI, Request, HTTPException, Query, UploadFile, File
from contextlib import asynccontextmanager
import httpx
import json
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from bson.objectid import ObjectId
from pathlib import Path

# python -m uvicorn main:app --reload --port 8000

clienteWiki: httpx.AsyncClient = None
clienteArticulo: httpx.AsyncClient = None
clienteComentario: httpx.AsyncClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Establecer conexión con los microservicios
    global clienteWiki, clienteArticulo, clienteComentario

    clienteWiki = httpx.AsyncClient(base_url="http://localhost:8001/api/v1")        # url local
    clienteArticulo = httpx.AsyncClient(base_url="http://localhost:8002/api/v1")    # url local
    clienteComentario = httpx.AsyncClient(base_url="http://localhost:8003/api/v1")  # url local

    # clienteWiki = httpx.AsyncClient(base_url="http://lawiki-modulo-wiki:8001/api/v1")        # url entorno Docker
    # clienteArticulo = httpx.AsyncClient(base_url="http://lawiki-modulo-articulo:8002/api/v1")    # url entorno Docker

    yield
    # Cerrar la conexión con los microservicios
    await clienteWiki.aclose()
    await clienteArticulo.aclose()
    await clienteComentario.aclose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


########## Metodos Complementarios ############

def getID(json: json):
    dict = json["_id"]
    id = dict["$oid"]

    return id

def getObjID(id: str):
    try:
        objID = ObjectId(id)
    except Exception as e:
        raise HTTPException(status_code=400, detail="Formato de ID inválido")

    return objID


###----------------------------------CRUD WIKIS-------------------------------------###


# PAGINA PRINCIPAL: DEVUELVE TODAS LAS WIKIS O DEVUELVE LAS WIKIS QUE CUMPLEN UNOS CRITERIOS
@app.get("/wikis")
async def getWikis(term: str = Query(None, min_length=1)):
    try:
        if term is None:
            respuesta = await clienteWiki.get("/wikis")
        else:
            respuesta = await clienteWiki.get("/wikis", params={"term": term})
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloWiki")


    return respuesta.json()

# PAGINA WIKI
@app.get("/wikis/{nombre}")
async def getWiki(nombre: str):
    try:
        respuesta = await clienteWiki.get(f"/wikis/{nombre}")
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloWiki")
    
    return respuesta.json()

# CREAR WIKI
@app.post( "/wikis")
async def crearWiki(request: Request):
    try:
        data = await request.json()
        respuesta = await clienteWiki.post("/wikis", json=data)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloWiki")

    return respuesta.json()

# ACTUALIZAR WIKI
@app.put("/wikis/{wikiID}")
async def actualizarWiki(request: Request, wikiID: str):
    try:
        data = await request.json()
        respuesta = await clienteWiki.put(f"/wikis/{wikiID}", json=data)
        respuesta.raise_for_status()
        return respuesta.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloWiki")


# ELIMINAR WIKI
@app.delete("/wikis/{wikiID}")
async def eliminarWiki(wikiID: str):
    try:
        respuesta = await clienteWiki.delete(f"/wikis/{wikiID}")
        respuesta.raise_for_status()        
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloWiki")

    return respuesta.json()


###--------------------------------CRUD ARTICULOS-----------------------------------###


# GET ARTICULOS DE UNA WIKI
@app.get("/wikis/{nombre}/articulos")
async def getArticulos(nombre: str, terminoDeBusqueda: str | None = None, usuario: str | None = None):
    wikiJSON = await getWiki(nombre)
    wikiID = getID(wikiJSON)

    try:
        query_params = {}
        query_params["wiki"] = wikiID
        if terminoDeBusqueda:
            query_params["terminoDeBusqueda"] = terminoDeBusqueda
        elif usuario:
            query_params["usuario"] = usuario

        respuesta = await clienteArticulo.get(f"/wikis/{nombre}/articulos", params=query_params)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")
    
    return respuesta.json()


# GET ARTICULO
@app.get("/wikis/{nombre}/articulos/{titulo}")
async def getArticulo(nombre : str, titulo : str):
    wikiJSON = await getWiki(nombre)
    wikiID = getID(wikiJSON)
    
    try:
        query_params = {}
        query_params["wiki"] = wikiID

        respuesta = await clienteArticulo.get(f"/wikis/{nombre}/articulos/{titulo}", params=query_params)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")
    
    return respuesta.json()


# CREAR ARTICULO
@app.post("/wikis/{nombre}/articulos")
async def crearArticulo(request: Request, nombre: str):
    wikiJSON = await getWiki(nombre)
    wikiID = getID(wikiJSON)
    
    try:
        data = await request.json()

        query_params = {}
        query_params["wiki"] = wikiID

        respuesta = await clienteArticulo.post(f"/wikis/{nombre}/articulos", params=query_params, json=data)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")
    
    return respuesta.json()


# ACTUALIZAR UN ARTÍCULO
@app.put("/wikis/{nombre}/articulos/{titulo}")
async def actualizarArticulo(request: Request, nombre: str, titulo: str):
    wikiJSON = await getWiki(nombre)
    wikiID = getID(wikiJSON)

    try:
        data = await request.json()

        query_params = {}
        query_params["wiki"] = wikiID

        respuesta = await clienteArticulo.put(f"/wikis/{nombre}/articulos/{titulo}", params=query_params, json=data)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")

    return respuesta.json()


# BORRAR UNA TODAS LAS VERSIONES DEL ARTÍCULO O SOLO UNA VERSION SI SE PASA ID
@app.delete("/wikis/{nombre}/articulos/{titulo}")
async def eliminarArticulo(nombre: str, titulo: str, id: str = Query(None, min_length=1)):
    try:
        query_params = {}
        if id is not None:
            query_params["id"] = id

        respuesta = await clienteArticulo.delete(f"/wikis/{nombre}/articulos/{titulo}", params=query_params)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")

    return respuesta.json()

@app.post("/subirImagen")
async def subirImagen(archivo : UploadFile = File(...)):
    try:
        files = {"archivo": (archivo.filename, archivo.file, archivo.content_type)}
        respuesta = await clienteArticulo.post(f"/subirImagen", files = files)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")
        
    return respuesta.json


###--------------------------------CRUD COMENTARIOS-----------------------------------###


# GET COMENTARIOS DE UN ARTICULO
@app.get("/wikis/{nombre}/articulos/{titulo}/comentarios")
async def getComentarios(nombre: str, titulo: str):
    articuloJSON = await getArticulo(nombre, titulo)
    articuloID = getID(articuloJSON)

    try:
        respuesta = await clienteComentario.get(f"/comentarios/articulo/{articuloID}")
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloComentario")
    
    return respuesta.json()


# CREAR COMENTARIO
@app.post("/wikis/{nombre}/articulos/{titulo}/comentarios")
async def crearComentario(request: Request, nombre: str, titulo: str):
    articuloJSON = await getArticulo(nombre, titulo)
    articuloID = getID(articuloJSON)

    try:
        data = await request.json()
        data["fecha"] = datetime.utcnow().isoformat()
        data["articulo_id"] = articuloID

        respuesta = await clienteComentario.post("/comentarios", json=data)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloComentario")
    
    return respuesta.json()


# ACTUALIZAR UN COMENTARIO
@app.put("/wikis/{nombre}/articulos/{titulo}/comentarios/{comentarioID}")
async def actualizarComentario(request: Request, nombre: str, titulo: str, comentarioID: str):
    articuloJSON = await getArticulo(nombre, titulo)
    articuloID = getID(articuloJSON)

    try:
        data = await request.json()
        data["fecha"] = datetime.utcnow().isoformat()
        data["articulo_id"] = articuloID

        respuesta = await clienteComentario.put(f"/comentarios/{comentarioID}", json=data)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloComentario")
    
    return respuesta.json()


# ELIMINAR UN COMENTARIO
@app.delete("/wikis/{nombre}/articulos/{titulo}/comentarios/{comentarioID}")
async def eliminarComentario(comentarioID: str):
    try:
        respuesta = await clienteComentario.delete(f"/comentarios/{comentarioID}")
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloComentario")
    
    return respuesta.json()
