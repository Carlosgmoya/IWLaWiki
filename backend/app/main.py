from fastapi import FastAPI, Request, HTTPException, Query
from contextlib import asynccontextmanager
import httpx
import json
from fastapi.middleware.cors import CORSMiddleware

# python -m uvicorn main:app --reload --port 8000

clienteWiki: httpx.AsyncClient = None
clienteArticulo: httpx.AsyncClient = None

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Establecer conexión con los microservicios
    global clienteWiki, clienteArticulo

    clienteWiki = httpx.AsyncClient(base_url="http://localhost:8001/api/v1")        # url local
    clienteArticulo = httpx.AsyncClient(base_url="http://localhost:8002/api/v1")    # url local

    # clienteWiki = httpx.AsyncClient(base_url="http://lawiki-modulo-wiki:8001/api/v1")        # url entorno Docker
    # clienteArticulo = httpx.AsyncClient(base_url="http://lawiki-modulo-articulo:8002/api/v1")    # url entorno Docker

    yield
    # Cerrar la conexión con los microservicios
    await clienteWiki.aclose()
    await clienteArticulo.aclose()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # URL del frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


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


########## Metodos Complementarios ############

def getWikiID(wikiJSON: json):
    wikiDict = wikiJSON["_id"]
    wikiID = wikiDict["$oid"]

    return wikiID


###--------------------------------CRUD ARTICULOS-----------------------------------###


# GET ARTICULOS DE UNA WIKI
@app.get("/wikis/{nombre}/articulos")
async def getArticulos(nombre: str, terminoDeBusqueda: str | None = None, usuario: str | None = None):
    wikiJSON = await getWiki(nombre)
    wikiID = getWikiID(wikiJSON)

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
    wikiID = getWikiID(wikiJSON)
    
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
    wikiID = getWikiID(wikiJSON)
    
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
    wikiID = getWikiID(wikiJSON)

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