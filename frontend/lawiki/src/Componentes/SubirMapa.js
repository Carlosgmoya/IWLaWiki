import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet"; // Leaflet is required for some additional functionality
import "leaflet/dist/leaflet.css"; // Import Leaflet CSS
import { toast } from "react-toastify";

function SubirMapa({ nombreWiki, tituloArticulo }) {
    const backendURL = process.env.REACT_APP_BACKEND_URL;
    
    const [mostrarSubirMapa, setMostrarSubirMapa] = useState(false);
    const [ubicacion, setUbicacion] = useState("");
    const [error, setError] = useState("");
    const [datosUbicacion, setDatosUbicacion] = useState([]);
    const [coordenadas, setCoordenadas] = useState(null);
    const [nombreUbicacion, setNombreUbicacion] = useState("");

    const handleAbrirSubirMapa = () => {
        setMostrarSubirMapa(true);
    }

    const handleCerrarSubirMapa = () => {
        setMostrarSubirMapa(false);
    }

    const handleInputChange = (event) => {
        setUbicacion(event.target.value);
    }

    const handleBuscarUbicacion = async () => {
        if (!ubicacion) {
            setError("Introduzca una ubicación para buscar");
            return;
        }

        setError("");
        let params = "";

        try {
            // Construct the URL with query parameters using URLSearchParams
            params = new URLSearchParams({
              q: ubicacion,
              format: 'json',
              addressdetails: '1', // Optional: includes address details in the response
            });
        } catch(error) {
            console.error("Error:", error);
            setError("Error inesperado al conectar con servidor URLSearchParams.");
        }

        try {
            const response = await fetch(`https://nominatim.openstreetmap.org/search?${params.toString()}`, {
                method: 'GET',
                headers: {
                    'User-Agent': 'laWiki/1.0 lawiki.iweb@gmail.com',
                },
            });

            if (!response.ok) {
                throw new Error('Respuesta del servidor no valida');
              }

            const respuestaJSON = await response.json();
            const ubi = respuestaJSON[0];

            setDatosUbicacion(respuestaJSON);
            setCoordenadas({
                lat: ubi.lat,
                lon: ubi.lon,
              });
            setNombreUbicacion(ubi.display_name);

        } catch(error) {
            console.error("Error:", error);
            setError("Error inesperado al conectar con servidor Nominatim.");
        }
    }

    const handleCambiarUbicacion = (latitud, longitud, nombre) => {
        setCoordenadas({
            lat: latitud,
            lon: longitud,
        });
        setNombreUbicacion(nombre);
    }

    const handleGuardarMapa = async () => {
        setMostrarSubirMapa(false);

        //borrar mapa anterior si hay
        try {
            const respuesta = await fetch(
                `${backendURL}/wikis/${nombreWiki}/articulos/${tituloArticulo}/mapas`
            );

            if (respuesta.ok) {
                const borrar = await fetch(
                    `${backendURL}/wikis/${nombreWiki}/articulos/${tituloArticulo}/mapas`,
                    {
                        method: "DELETE"
                    }
                );
            }
        } catch(error) {
            console.error("Error:", error);
            setError("Error inesperado al conectar con backend.");
        }

        const datos = {
            latitud: coordenadas.lat,
            longitud: coordenadas.lon,
            nombreUbicacion: nombreUbicacion,
        }

        try {
            const respuesta = await fetch(
                `${backendURL}/wikis/${nombreWiki}/articulos/${tituloArticulo}/mapas`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datos),
                }
            );

            if (respuesta.ok) {
                toast.success("Mapa actualizado con éxito", {
                            position: "top-right",
                            autoClose: 3000, // Auto close after 3 seconds
                            hideProgressBar: false,
                            closeOnClick: true,
                            pauseOnHover: true,
                            draggable: true,
                            progress: undefined,
                          });
            }
        } catch(error) {
            console.error("Error:", error);
            setError("Error inesperado al conectar con backend.");
        }
    }

    const MapComponent = ({ coordinates, locationName }) => {
        // Check if coordinates exist
        if (!coordinates) {
          return <div>Loading map...</div>;
        }
      
        const { lat, lon } = coordinates;
      
        return (
          <MapContainer center={[lat, lon]} zoom={13} style={{ height: '400px', width: '50%' }}>
            {/* Add OpenStreetMap tiles */}
            <TileLayer
              url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
            />
            {/* Add a Marker to show the location */}
            <Marker position={[lat, lon]}>
              <Popup>
                <span>{locationName}</span>
              </Popup>
            </Marker>
          </MapContainer>
        );
      };
      

    return (<>
        { !mostrarSubirMapa ? ( 
            <>
                <button title="Añadir ubicación" className="irASubirMapa" onClick={handleAbrirSubirMapa}>
                    <img src="/Iconos/IconoAddMapa.svg" alt="Añadir ubicación" />
                </button>
            </>
        ) : (
            <>
                Ubicación:
                <input 
                    type="text"
                    value={ubicacion}
                    onChange={handleInputChange}
                    placeholder="Introduce ubicación...">
                </input>
                <button onClick={handleBuscarUbicacion}>Buscar</button>
                <button onClick={handleCerrarSubirMapa}>Cancelar</button>
                {error && <div style={{ color: 'red' }}>{error}</div>}

                <div>
                    {datosUbicacion.length > 0 ? (
                    <ul>
                        {datosUbicacion.map((location) => (
                        <li key={location.place_id}>
                            <button onClick={() => handleCambiarUbicacion(location.lat, location.lon, location.display_name)}>
                                {location.display_name}
                            </button>
                        </li>
                        ))}
                    </ul>
                    ) : (
                    <p>Ninguna ubicación encontrada</p>
                    )}
                </div>
                {coordenadas && (
                    <div>
                        <MapComponent coordinates={coordenadas} locationName={nombreUbicacion} />
                        <button onClick={handleGuardarMapa}>Confirmar</button>
                    </div>
                )}
            </>
            )
        }
    </>);
}

export default SubirMapa;