import dropbox
import requests

APP_KEY = 'jceh9h8d9377e2c'
APP_SECRET = 'ruitu5uzew9ernf'
REFRESH_TOKEN = 'jHTk0YhbHIYAAAAAAAAAARecc2rKN5UzfwRfvFh6iIlxGCRRGP9i9Cp5TEeRnDo0'

def renovar_access_token():
    url = "https://api.dropbox.com/oauth2/token"
    data = {
        "grant_type": "refresh_token",
        "refresh_token": REFRESH_TOKEN,
        "client_id": APP_KEY,
        "client_secret": APP_SECRET,
    }
    response = requests.post(url, data=data)
    if response.status_code == 200:
        access_token = response.json().get('access_token')
        print(f"Nuevo Access Token: {access_token}")
        return access_token
    else:
        print(f"Error al renovar el token: {response.json()}")
        return None
ACCESS_TOKEN = renovar_access_token()
if ACCESS_TOKEN:
    dbx = dropbox.Dropbox(ACCESS_TOKEN)
else:
    print("No se pudo obtener un Access Token válido.")

dbx = dropbox.Dropbox(ACCESS_TOKEN)

def generarNombreUnico(ruta_remota):
    """Genera un nombre único si el archivo ya existe en Dropbox."""
    try:
        dbx.files_get_metadata(ruta_remota)
        # Si llegamos aquí, el archivo ya existe, generamos un nuevo nombre
        nombre, extension = ruta_remota.rsplit('.', 1) if '.' in ruta_remota else (ruta_remota, '')
        contador = 1
        while True:
            nuevoNombre = f"{nombre} ({contador})"
            if extension:
                nuevoNombre += f".{extension}"
            nuevoRutaRemota = f"/{nuevoNombre}"
            try:
                dbx.files_get_metadata(nuevoRutaRemota)
            except dropbox.exceptions.ApiError:
                # Si no existe, devolvemos el nuevo nombre
                return nuevoRutaRemota
            contador += 1
    except dropbox.exceptions.ApiError:
        # Si no existe, devolvemos el nombre original
        return ruta_remota

def subirImagenDropbox(rutaLocal, rutaRemota):
    rutaRemota = generarNombreUnico(rutaRemota)
    try :
        with open(rutaLocal, 'rb') as archivo:
            dbx.files_upload(archivo.read(), rutaRemota, mode=dropbox.files.WriteMode.overwrite)
            print(f"Imagen subida a {rutaRemota}")
    except FileNotFoundError:
        print("Archivo no encontrado. Asegúrate de seleccionar un archivo.")
    except Exception as e:
        print(f"Error al subir el archivo: {e}")


def obtenerEnlaceImagen(rutaRemota):
    try:
        # Crear enlace compartido para el archivo
        enlaceCompartido = dbx.sharing_create_shared_link_with_settings(rutaRemota).url
        # Modificar el enlace para que sea un enlace directo (descarga)
        if '?dl=0' in enlaceCompartido:
            enlaceDescarga = enlaceCompartido.replace('?dl=0', '?raw=1')
        else:
            # Si el enlace no tiene 'dl=0', añadir 'raw=1' correctamente
            enlaceDescarga = f"{enlaceCompartido}&raw=1"
        return enlaceDescarga
    except dropbox.exceptions.ApiError as e:
        print(f"Error al obtener el enlace: {e}")
        return None