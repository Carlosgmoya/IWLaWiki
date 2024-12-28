import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import { useSesion } from "../Login/authContext";
import { tienePermiso } from "../Login/auth";

import "../Estilos/VentanaHistorial.css";

function VentanaHistorial() {
    const backendURL = process.env.REACT_APP_BACKEND_URL;

    const { rolUsuario } = useSesion();

    const { nombre } = useParams();
    const { titulo } = useParams();
    const [listaArticulos, setListaArticulos] = useState(null);
    const [listaEditores, setListaEditores] = useState(null);

    const options = {
        year: "numeric",
        month: "long",
        day: "numeric"
    };

    useEffect(() => {
        const fetchData = async () => {
            try {
                const respuesta1 = await fetch(`${backendURL}/wikis/${nombre}/articulos/${titulo}`);
                const articuloJson = await respuesta1.json();

                const respuesta2 = await fetch(`${backendURL}/wikis/${nombre}/articulos/${titulo}/versiones`);
                const listaJson = await respuesta2.json();
                let listaArticulos = listaJson.sort((a, b) => b.fecha.$date - a.fecha.$date);
                listaArticulos.unshift(articuloJson);
                console.log(listaArticulos);
                setListaArticulos(listaArticulos);
            } catch (error) {
                console.error("Error al obtener datos:", error);
            }
        };
        fetchData();
    }, [backendURL, nombre, titulo]);

    return (<>
        <div className="cabeceraWiki">
            <h1 className="nombreWiki"><Link to={`/wikis/${nombre || 'defaultNombre'}`}>{nombre}</Link></h1>
        </div>

        <div className="historial">
            <div className="cabeceraHistorial">
                <h1 className="tituloHistorial">Historial de {titulo}</h1>
            </div>
            <div className="cuerpoHistorial">
            {listaArticulos === null || listaEditores === null ? (
                <p>Cargando...</p>
            ) : (
                <ul>
                  {listaArticulos.map((articulo, index) => (
                    <li key={index}>
                      <h4>{new Date(articulo["fecha"]["$date"]).toLocaleDateString("es-ES", options)}, {new Date(articulo["fecha"]["$date"]).toLocaleTimeString("es-ES")}</h4>
                    </li>
                  ))}
                </ul>
            )}
            </div>
        </div>
    </>)
}

export default VentanaHistorial;