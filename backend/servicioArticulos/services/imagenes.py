import dropbox
import requests
from tkinter import Tk
from tkinter.filedialog import askopenfilename

APP_KEY = '550i2tid5x9fltn'
APP_SECRET = 'kzwo0g16zld74yi'
REFRESH_TOKEN = 'Pj7dO7dLu7QAAAAAAAAAAXv2H57ljLRGU3W7fm_os_z1liNm-rwcbUPehWFomQlz'

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

def seleccionarArchivo():
    # Crear una ventana oculta de Tkinter
    root = Tk()
    root.withdraw()  # Oculta la ventana principal
    # Abre el diálogo para seleccionar un archivo
    rutaArchivo = askopenfilename(title="Seleccionar archivo para subir a Dropbox")
    return rutaArchivo

def generar_nombre_unico(ruta_remota):
    """Genera un nombre único si el archivo ya existe en Dropbox."""
    try:
        dbx.files_get_metadata(ruta_remota)
        # Si llegamos aquí, el archivo ya existe, generamos un nuevo nombre
        nombre, extension = ruta_remota.rsplit('.', 1) if '.' in ruta_remota else (ruta_remota, '')
        contador = 1
        while True:
            nuevo_nombre = f"{nombre} ({contador})"
            if extension:
                nuevo_nombre += f".{extension}"
            nuevo_ruta_remota = f"/{nuevo_nombre}"
            try:
                dbx.files_get_metadata(nuevo_ruta_remota)
            except dropbox.exceptions.ApiError:
                # Si no existe, devolvemos el nuevo nombre
                return nuevo_ruta_remota
            contador += 1
    except dropbox.exceptions.ApiError:
        # Si no existe, devolvemos el nombre original
        return ruta_remota

def subirImagenDropbox(rutaLocal, rutaRemota):
    rutaRemota = generar_nombre_unico(rutaRemota)
    try :
        with open(rutaLocal, 'rb') as archivo:
            dbx.files_upload(archivo.read(), rutaRemota, mode=dropbox.files.WriteMode.overwrite)
            print(f"Imagen subida a {rutaRemota}")
    except FileNotFoundError:
        print("Archivo no encontrado. Asegúrate de seleccionar un archivo.")
    except Exception as e:
        print(f"Error al subir el archivo: {e}")


def obtenerEnlaceImagen(ruta_remota):
    try:
        # Crear enlace compartido para el archivo
        enlace_compartido = dbx.sharing_create_shared_link_with_settings(ruta_remota).url
        # Modificar el enlace para que sea un enlace directo (descarga)
        enlace_descarga = enlace_compartido.replace('?dl=0', '?raw=1')
        return enlace_descarga
    except dropbox.exceptions.ApiError as e:
        print(f"Error al obtener el enlace: {e}")
        return None