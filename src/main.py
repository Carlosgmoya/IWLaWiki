from fastapi import FastAPI

from bson.json_util import dumps
import json

api = FastAPI()

# ejecutar con    python -m uvicorn main:api --reload --port 8000

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


# GET WIKI

@api.get("/{n}")
async def getWiki(n : str):
    result = BD_wiki.find_one({ "nombre" : n })
    result_json = None
    if result:
        result_json = dumps(result)
    else:
        print("No se encontro ninguna entidad")

    return result_json

# GET ARTICULO