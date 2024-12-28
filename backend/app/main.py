from fastapi import FastAPI, Request, HTTPException, Query, UploadFile, File, Form
from contextlib import asynccontextmanager
import httpx
from httpx import Timeout
import json
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime
from bson.objectid import ObjectId

# python -m uvicorn main:app --reload --port 8000

clienteWiki: httpx.AsyncClient = None
clienteArticulo: httpx.AsyncClient = None
clienteComentario: httpx.AsyncClient = None
clienteUsuario: httpx.AsyncClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Establecer conexión con los microservicios
    global clienteWiki, clienteArticulo, clienteComentario, clienteUsuario

    clienteWiki = httpx.AsyncClient(base_url="http://localhost:8001/api/v1", timeout=Timeout(10.0))        # url local
    clienteArticulo = httpx.AsyncClient(base_url="http://localhost:8002/api/v1")    # url local
    clienteComentario = httpx.AsyncClient(base_url="http://localhost:8003/api/v1")  # url local
    clienteUsuario = httpx.AsyncClient(base_url="http://localhost:8004/api/v1")     # url local

    #clienteWiki = httpx.AsyncClient(base_url="http://lawiki-modulo-wiki:8001/api/v1", timeout=Timeout(10.0))        # url entorno Docker
    #clienteArticulo = httpx.AsyncClient(base_url="http://lawiki-modulo-articulo:8002/api/v1")    # url entorno Docker
    #clienteComentario = httpx.AsyncClient(base_url="http://lawiki-modulo-comentario:8003/api/v1")    # url entorno Docker
    #clienteUsuario = httpx.AsyncClient(base_url="http://lawiki-modulo-usuario:8004/api/v1")    # url entorno Docker

    yield
    # Cerrar la conexión con los microservicios
    await clienteWiki.aclose()
    await clienteArticulo.aclose()
    await clienteComentario.aclose()
    await clienteUsuario.aclose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://react-app:80"],  # URL del frontend
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
async def crearWiki(
    nombre: str = Form(...),
    descripcion: str = Form(...),
    archivoP: UploadFile = File(...),
    archivoC: UploadFile = File(...),):
    try:
        data = {
            "nombre": nombre,
            "descripcion": descripcion,
        }
        # Crear el payload de archivos
        files = {
            "archivoP": (archivoP.filename, archivoP.file, archivoP.content_type),
            "archivoC": (archivoC.filename, archivoC.file, archivoC.content_type),
        }
        archivoP.file.seek(0)
        archivoC.file.seek(0)

        # Hacer la solicitud
        respuesta = await clienteWiki.post("/wikis", data=data, files=files)
        respuesta.raise_for_status()

        try:
            return respuesta.json()
        except ValueError as json_error:
            # Si la respuesta no es JSON, devolver un error
            raise HTTPException(
                status_code=500,
                detail=f"Error al interpretar la respuesta del servidor: {str(json_error)}",
            )

    except httpx.HTTPStatusError as e:
        # Capturar errores HTTP específicos
        raise HTTPException(
            status_code=e.response.status_code,
            detail=f"Error al crear la Wiki: {e.response.text}",
        )
    except Exception as e:
        # Capturar cualquier otro error
        raise HTTPException(
            status_code=500,
            detail=f"Error interno al crear la Wiki: {str(e)}",
        )

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
    
    respuestaJSON = respuesta.json()

    return "Artículo actualizado con éxito"


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
        
    return respuesta.text

@app.get("/wikis/{nombre}/articulos/{titulo}/versiones")
async def todasVersiones(nombre : str, titulo : str):
    articuloJSON = await getArticulo(nombre, titulo)
    articuloID = getID(articuloJSON)
    
    try:
        query_params = {}
        query_params["titulo"] = articuloID

        respuesta = await clienteArticulo.get(f"/wikis/{nombre}/articulos/{titulo}/versiones", params=query_params)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")
    
    return respuesta.json()

@app.put("/wikis/{nombre}/articulos/{titulo}/cambiarVersion")
async def cambiarVersion(nombre : str, titulo : str, idVersion : str):
    articuloJSON = await getArticulo(nombre, titulo)
    articuloID = getID(articuloJSON)
    articuloVersionID = getObjID(idVersion)

    try:
        query_params = {}
        query_params["idActual"] = articuloID
        query_params["idVolver"] = articuloVersionID

        respuesta = await clienteArticulo.put(f"/wikis/{nombre}/articulos/{titulo}/cambiarVersion", params=query_params)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")
    
    return respuesta.json()

# TRADUCIR UN ARTÍCULO
@app.put("/wikis/{nombre}/articulos/{titulo}/traducir")
async def traducirArticulo(request: Request, nombre: str, titulo: str, idioma : str):
    wikiJSON = await getWiki(nombre)
    wikiID = getID(wikiJSON)


    try:
        query_params = {}
        query_params["wiki"] = wikiID
        query_params["idioma"] = idioma

        respuesta = await clienteArticulo.put(f"/wikis/{nombre}/articulos/{titulo}/traducir", params=query_params)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")
    

    return "Artículo traducido con éxito"



###--------------------------------CRUD MAPAS-----------------------------------###
# GET MAPA
@app.get("/wikis/{nombre}/articulos/{titulo}/mapas")
async def getMapa(nombre : str, titulo : str):
    articuloJSON = await getArticulo(nombre, titulo)
    articuloID = getID(articuloJSON)
    
    try:
        query_params = {}
        query_params["art"] = articuloID

        respuesta = await clienteArticulo.get(f"/wikis/{nombre}/articulos/{titulo}/mapa", params=query_params)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")
    
    return respuesta.json()

# CREAR MAPA
@app.post("/wikis/{nombre}/articulos/{titulo}/mapas")
async def crearMapa(request: Request, nombre: str, titulo : str):
    articuloJSON = await getArticulo(nombre, titulo)
    articuloID = getID(articuloJSON)
    
    try:
        data = await request.json()

        query_params = {}
        query_params["art"] = articuloID

        respuesta = await clienteArticulo.post(f"/wikis/{nombre}/articulos/{titulo}/mapas", params=query_params, json=data)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")
    
    return respuesta.json()

# ACTUALIZAR MAPA
@app.put("/wikis/{nombre}/articulos/{titulo}/mapas")
async def actualizarMapa(request: Request, nombre: str, titulo : str):
    articuloJSON = await getArticulo(nombre, titulo)
    articuloID = getID(articuloJSON)
    mapaJSON = await getMapa(nombre, titulo)
    mapaID = getID(mapaJSON)
    
    try:
        data = await request.json()

        query_params = {}
        query_params["mapa"] = mapaID
        query_params["art"] = articuloID

        respuesta = await clienteArticulo.put(f"/wikis/{nombre}/articulos/{titulo}/mapas", params=query_params, json=data)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")
    
    return respuesta.json()

# BORRAR MAPA
@app.delete("/wikis/{nombre}/articulos/{titulo}/mapas")
async def eliminarMapa(nombre: str, titulo: str):
    articuloJSON = await getArticulo(nombre, titulo)
    articuloID = getID(articuloJSON)

    try:
        query_params = {}
        query_params["id"] = articuloID

        respuesta = await clienteArticulo.delete(f"/wikis/{nombre}/articulos/{titulo}/borrarMapa", params=query_params)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloArticulo")

    return respuesta.json()


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

# GET COMENTARIOS DE UN USUARIO EN UN ARTICULO
@app.get("/wikis/{nombre}/articulos/{titulo}/comentarios/{usuario}")
async def getComentariosPorArticuloYUsuario(nombre: str, titulo: str, usuario: str):
    articuloJSON = await getArticulo(nombre, titulo)
    articuloID = getID(articuloJSON)

    try:
        respuesta = await clienteComentario.get(f"/comentarios/articulo/{articuloID}/usuario/{usuario}")
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


###----------------------------------CRUD USUARIOS-------------------------------------###


# GET USUARIO POR ID
@app.get("/usuarios/id/{usuarioID}")
async def getUsuariosPorId(usuarioID: str):
    try:
        respuesta = await clienteUsuario.get(f"/usuarios/id/{usuarioID}")
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloUsuario")

    return respuesta.json()

# GET USUARIO POR EMAIL
@app.get("/usuarios/email/{usuarioEmail}")
async def getUsuariosPorId(usuarioEmail: str):
    try:
        respuesta = await clienteUsuario.get(f"/usuarios/email/{usuarioEmail}")
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloUsuario")

    return respuesta.json()

# CREAR NUEVO USUARIO
@app.post("/usuarios/")
async def crearUsuario(request: Request):
    try:
        data = await request.json()
        # por defecto, el nuevo usuario no es admin
        data["esAdmin"] = False
        respuesta = await clienteUsuario.post("/usuarios", json=data)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloUsuario")
    
    return respuesta.json()

###----------------------------------CRUD VALORACIONES-------------------------------------###


@app.post("/valoraciones")
async def crearValoracion(request: Request):
    try:
        data = await request.json()
        respuesta = await clienteUsuario.post("/valoraciones", json=data)
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloUsuario")
    
    return respuesta.json()

# GET MEDIA VALORACIONES DE USUARIO POR EMAIL
@app.get("/valoracion/{usuario}")
async def getValoracionDeUsuario(usuario: str):
    try:
        respuesta = await clienteUsuario.get(f"/valoracion/{usuario}")
        respuesta.raise_for_status()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloUsuario")

    return respuesta.json()
