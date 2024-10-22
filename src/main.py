from fastapi import FastAPI

api = FastAPI()

# ejecutar con    python -m uvicorn main:api --reload --port 8000

path = "/api/v1/"



@api.get("/laWiki/{nombre}")                    # endpoint: laWiki/{nombre}    (Parámetro de Path)
async def hola(nombre : str):

    return {"Bienvenido a: " + nombre}