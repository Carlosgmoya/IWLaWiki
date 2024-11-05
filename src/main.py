from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from typing import Any
from bson import json_util
from bson.objectid import ObjectId
from typing import List
import json

api = FastAPI()
api.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# ejecutar con  cd src -> python -m uvicorn main:api --reload --port 8000

# conexion al servidor MongoDB

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://admin:admin@cluster0.mw2bq.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

# Base de Datos

database = client["laWiki"]

BD_wiki = database["wiki"]
BD_articulo = database["articulo"]

# EJEMPLO

@api.get("/laWiki/{nombre}")                    # endpoint: laWiki/{nombre}    (Parámetro de Path)
async def hola(nombre : str):

    return {"Bienvenido a: " + nombre}


# PAGINA PRINCIPAL

@api.get("/", response_class=HTMLResponse)
async def getIndex(request : Request):
    wikis_doc = BD_wiki.find().sort({"nombre":1})
    wikis_json = [json.loads(json_util.dumps(doc)) for doc in wikis_doc]    # collection.find() retrieves documents in BSON format from MongoDB.
                                                                            # json_util.dumps(doc) converts BSON documents, including ObjectId fields, to JSON strings.
                                                                            # json.loads(...) transforms each document back into a Python dictionary, so it’s compatible with FastAPI's JSON response model.
    return templates.TemplateResponse(
        "index.html",
        {"request": request,
         "wikis": wikis_json}
        )

# GET WIKI

@api.get("/{n}", response_class=HTMLResponse)
async def getWiki(request: Request, n : str):
    wiki_doc = BD_wiki.find_one({ "nombre" : n })

    if wiki_doc is None:
        raise HTTPException(status_code=404, detail="Item not found")
    
    wiki_json = json.loads(json_util.dumps(wiki_doc))

    return templates.TemplateResponse(
        "wiki.html",
        {"request": request,
         "wiki": wiki_json}
    )

# GET ARTICULO