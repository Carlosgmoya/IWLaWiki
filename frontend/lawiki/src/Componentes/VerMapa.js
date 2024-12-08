import React, { useState, useEffect, useCallback } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";

function VerMapa({ nombreWiki, tituloArticulo }) {

    const [coordenadas, setCoordenadas] = useState(null);
    const [nombreUbicacion, setNombreUbicacion] = useState("");

    const fetchMapa = useCallback(async () => {
        try {
            const response = await fetch(
                `http://127.0.0.1:8000/wikis/${nombreWiki}/articulos/${tituloArticulo}/mapas`
            );
            const datos = await response.json();
            setCoordenadas({
                lat: datos.latitud,
                lon: datos.longitud,
            });
            setNombreUbicacion(datos.nombreUbicacion);
        } catch (error) {
            console.error("Error al obtener los detalles de mapa:", error);
        }
    }, [nombreWiki, tituloArticulo]);

    useEffect(() => {
        fetchMapa();
    }, [fetchMapa])

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

    return <MapComponent coordinates={coordenadas} locationName={nombreUbicacion} />;
}

export default VerMapa;