import React, { useState, useEffect, useCallback } from "react";
import { MapContainer, TileLayer, Marker, Popup } from "react-leaflet";
import L from "leaflet"; // Leaflet is required for some additional functionality

function VerMapa({ nombreWiki, tituloArticulo }) {
    const backendURL = process.env.REACT_APP_BACKEND_URL;

    const [coordenadas, setCoordenadas] = useState(null);
    const [nombreUbicacion, setNombreUbicacion] = useState("");

    const marker = L.icon({
        iconUrl: "/Iconos/Marker.svg",
        iconSize: [32, 32],
        iconAnchor: [16, 32],
        popupAnchor: [0, -32],
    });

    const fetchMapa = useCallback(async () => {
        try {
            const respuesta = await fetch(
                `${backendURL}/wikis/${nombreWiki}/articulos/${tituloArticulo}/mapas`
            );
            if (respuesta.ok) {
              const datos = await respuesta.json();
              setCoordenadas({
                  lat: datos.latitud,
                  lon: datos.longitud,
              });
              setNombreUbicacion(datos.nombreUbicacion);
            }
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
          return (
            <img className="mapaDefault" title="Ubicación no añadida" src="/Iconos/NoUbicacion.svg" alt="No ubicación"/>
          );
        }
      
        const { lat, lon } = coordinates;
      
        return (
          <MapContainer center={[lat, lon]} zoom={13} style={{ height: '400px', width: '100%', margin: '0 auto' }}>
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
        );
      };

    return <MapComponent coordinates={coordenadas} locationName={nombreUbicacion} />;
}

export default VerMapa;