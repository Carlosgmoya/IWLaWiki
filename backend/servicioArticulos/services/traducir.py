import requests

KEY = "8TmUJuVqNw8u2qHm4I44W9fWXqqXjj82yhMFy7837DC4vZ8pTRIBJQQJ99ALAC5RqLJXJ3w3AAAbACOGXx2Y"
ENDPOINT = "https://api.cognitive.microsofttranslator.com/"
REGION = "westeurope"

def traducirTexto(text, target_language):
    # Configuración de la solicitud
    path = '/translate'
    url = f"{ENDPOINT}{path}"
    params = {
        'api-version': '3.0',
        'to': target_language
    }
    headers = {
        'Ocp-Apim-Subscription-Key': KEY,
        'Ocp-Apim-Subscription-Region': REGION,
        'Content-Type': 'application/json'
    }
    body = [{
        'text': text
    }]

    # Realiza la solicitud POST
    response = requests.post(url, params=params, headers=headers, json=body)

    # Manejo de la respuesta
    if response.status_code == 200:
        result = response.json()
        # Devuelve el texto traducido
        return result[0]['translations'][0]['text']
    else:
        raise Exception(f"Error {response.status_code}: {response.text}")

