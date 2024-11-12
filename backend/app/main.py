from fastapi import FastAPI, Request, HTTPException, Query
from contextlib import asynccontextmanager
import httpx

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

# PAGINA PRINCIPAL: DEVUELVE TODAS LAS WIKIS O DEVUELVE LAS WIKIS QUE CUMPLEN UNOS CRITERIOS
@app.get("/wikis")
async def getWikis(term: str = Query(None, min_length=1)):
    try:
        if term is None:
            respuesta = await clienteWiki.get("/wikis")
        else:
            respuesta = await clienteWiki.get("/wikis", params={"term": term})
        respuesta.raise_for_status()
        wikisJSON = respuesta.json()
        return wikisJSON
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloWiki")


# PAGINA WIKI
@app.get("/wikis/{nombre}")
async def getWiki(nombre: str):
    try:
        respuesta = await clienteWiki.get(f"/wikis/{nombre}")
        respuesta.raise_for_status()
        return respuesta.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloWiki")
    

# CREAR WIKI
@app.post( "/wikis")
async def crearWiki(request: Request):
    try:
        data = await request.json()
        respuesta = await clienteWiki.post("/wikis", json=data)
        respuesta.raise_for_status()
        return respuesta.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloWiki")


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
        return respuesta.json()
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail="No se ha conseguido establecer conexión con moduloWiki")
