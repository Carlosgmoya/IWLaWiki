import React, { useState } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet"; // Leaflet is required for some additional functionality
import "leaflet/dist/leaflet.css"; // Import Leaflet CSS
import { toast } from "react-toastify";

import '../Estilos/SubirMapa.css';

function SubirMapa({ nombreWiki, tituloArticulo }) {
    const backendURL = process.env.REACT_APP_BACKEND_URL;

    const [mostrarSubirMapa, setMostrarSubirMapa] = useState(false);
    const [ubicacion, setUbicacion] = useState("");
    const [error, setError] = useState("");
    const [datosUbicacion, setDatosUbicacion] = useState([]);
    const [coordenadas, setCoordenadas] = useState(null);
    const [nombreUbicacion, setNombreUbicacion] = useState("");

    const marker = L.icon({
        iconUrl: "/Iconos/Marker.svg",
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32],
    });

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
        } catch (error) {
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

        } catch (error) {
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

        //actualizar mapa anterior si hay
        try {
            const datos = {
                latitud: coordenadas.lat,
                longitud: coordenadas.lon,
                nombreUbicacion: nombreUbicacion,
            }

            const respuesta = await fetch(
                `${backendURL}/wikis/${nombreWiki}/articulos/${tituloArticulo}/mapas`
            );

            if (respuesta.ok) {
                const actualizar = await fetch(
                    `${backendURL}/wikis/${nombreWiki}/articulos/${tituloArticulo}/mapas`,
                    {
                      method: "PUT",
                      headers: { "Content-Type": "application/json" },
                      body: JSON.stringify(datos),
                    }
                  );

                  toast.success("Mapa actualizado con éxito", {
                    position: "top-right",
                    autoClose: 3000, // Auto close after 3 seconds
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
            } else {
                console.log(JSON.stringify(datos));
                const crear = await fetch(
                    `${backendURL}/wikis/${nombreWiki}/articulos/${tituloArticulo}/mapas`,
                    {
                        method: "POST",
                        headers: { "Content-Type": "application/json" },
                        body: JSON.stringify(datos),
                    }
                );
    
                if (respuesta.ok) {
                    toast.success("Mapa añadido con éxito", {
                        position: "top-right",
                        autoClose: 3000, // Auto close after 3 seconds
                        hideProgressBar: false,
                        closeOnClick: true,
                        pauseOnHover: true,
                        draggable: true,
                        progress: undefined,
                    });
                }
            }
        } catch (error) {
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
            <div className="contenedorMapaBuscado">
                <MapContainer center={[lat, lon]} zoom={13} style={{ height: '400px', width: '100%' }}>
                    {/* Add OpenStreetMap tiles */}
                    <TileLayer
                        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
                    />
                    {/* Add a Marker to show the location */}
                    <Marker position={[lat, lon]} icon={marker}>
                        <Popup>
                            <span>{locationName}</span>
                        </Popup>
                    </Marker>
                </MapContainer>
            </div>
        );
    };


    return (<>
        {!mostrarSubirMapa ? (
            <div className="contenedorIrASubirMapa">
                <button title="Añadir ubicación" className="irASubirMapa" onClick={handleAbrirSubirMapa}>
                    <img src="/Iconos/IconoAddMapa.svg" alt="Añadir ubicación" />
                    <p>Adjunta una ubicación al artículo</p>
                </button>
            </div>
        ) : (
            <div className="contenedorBuscarMapa">
                <div className="buscadorUbicacion">
                    <input
                        type="text"
                        value={ubicacion}
                        onChange={handleInputChange}
                        placeholder="Introduce ubicación...">
                    </input>
                    <button onClick={handleBuscarUbicacion}>
                        <img title="Buscar" src="/Iconos/IconoBuscar.svg" alt="Buscar ubicación" />
                    </button>
                    <button onClick={handleCerrarSubirMapa}>
                        <img title="Cerrar" src="/Iconos/IconoCancelar.svg" alt="Cancelar búsqueda de ubicación" />
                    </button>
                </div>
                {error && <div style={{ color: 'red' }}>{error}</div>}

                <div>
                    {datosUbicacion.length > 0 ? (
                        <ul className="listaUbicaciones">
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
                        <div className="contenedorBotonConfirmarUbicacion">
                            <button className="botonConfirmarUbicacion" onClick={handleGuardarMapa}>
                                <img title="Confirmar ubicación" src="/Iconos/IconoSubirUbicacion.svg" alt="Confirmar" />
                            </button>
                        </div>
                    </div>
                )}
            </div>
        )
        }
    </>);
}

export default SubirMapa;