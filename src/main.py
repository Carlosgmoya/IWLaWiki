from fastapi import FastAPI

api = FastAPI()

# ejecutar con    python -m uvicorn main:api --reload --port 8000

# conexion a base de datos

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



@api.get("/laWiki/{nombre}")                    # endpoint: laWiki/{nombre}    (Parámetro de Path)
async def hola(nombre : str):

    return {"Bienvenido a: " + nombre}