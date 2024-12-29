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
    const [articuloActual, setArticuloActual] = useState(null);
    const [listaEditores, setListaEditores] = useState(null);
    const [mensaje, setMensaje] = useState("");
    const [mostrarHistorial, setMostrarHistorial] = useState(true);

    const options = {
        year: "numeric",
        month: "long",
        day: "numeric"
    };

    const fechaLocale = function(timestamp) {
        return new Date(timestamp).toLocaleDateString("es-ES", options) + ", " + new Date(timestamp).toLocaleTimeString("es-ES")
    }

    const byteSize = function(string) {
        return new Blob([string]).size;
    }

    const mensajeCambio = function(numero) {
        if (numero > 0) return "Se añadirán " + numero + " bytes";
        else if (numero < 0) return "Se eliminarán " + Math.abs(numero) + " bytes";
        else return "No se modificará el tamaño";
    }

    const revertirVersion = async(nuevaVersionId) => {
        const respuesta = await fetch(`${backendURL}/wikis/${nombre}/articulos/${titulo}/cambiarVersion?idVersion=${nuevaVersionId}`, {
            method: "PUT"
        });
        setMostrarHistorial(false);
        if (respuesta.ok) {
            setMensaje("El artículo ha sido revertido a la versión especificada.")
        } else {
            setMensaje("No se ha podido revertir el artículo a la versión especificada.")
        }
    };

    useEffect(() => {
        const fetchData = async() => {
            try {
                const respuesta1 = await fetch(`${backendURL}/wikis/${nombre}/articulos/${titulo}`);
                const articuloJson = await respuesta1.json();
                setArticuloActual(articuloJson);

                const respuesta2 = await fetch(`${backendURL}/wikis/${nombre}/articulos/${titulo}/versiones?idioma=${articuloJson.idioma}`);
                let listaArticulos = [];
                if (respuesta2.status !== 404) {
                    const listaJson = await respuesta2.json();
                    listaArticulos = listaJson.sort((a, b) => new Date(b.fecha.$date) - new Date(a.fecha.$date));
                }
                setListaArticulos(listaArticulos);

                let listaEditores = []
                for (const articulo of listaArticulos) {
                    const usuario = await fetch(`${backendURL}/usuarios/id/${articulo.creador.$oid}`);
                    const usuarioJson = await usuario.json();
                    listaEditores.push(usuarioJson.nombre);
                }
                setListaEditores(listaEditores);
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

        {tienePermiso(rolUsuario, "editarArticuloMio") &&
        <>
        {mostrarHistorial &&
        <div className="historial">
            <div className="cabeceraHistorial">
                <h1 className="tituloHistorial">Versiones anteriores de {titulo}</h1>
            </div>
            <div className="cuerpoHistorial">
            {listaArticulos === null || listaEditores === null ? (
                <p>Cargando...</p>
            ) : (
                <>
                {listaArticulos.length === 0 ? (
                    <p>No hay versiones anteriores del artículo</p>
                ) : (
                <ul>
                {listaArticulos.map((articulo, index) => (
                  <li key={index}>
                    <h3>{fechaLocale(articulo["fecha"]["$date"])} por <Link to={`/usuario/${listaEditores[index]}`}>{listaEditores[index]}</Link></h3>
                  {articulo.fecha.$date === articulo.fechaCreacion.$date ? (
                    <p>{mensajeCambio(byteSize(articulo.contenido) - byteSize(articuloActual.contenido))} (artículo creado)</p>
                  ) : (
                    <>
                    <p>{mensajeCambio(byteSize(articulo.contenido) - byteSize(articuloActual.contenido))} ({byteSize(articulo.contenido)} bytes)</p>
                    </>
                  )}
                    <button onClick={() => revertirVersion(articulo._id.$oid)}>Revertir</button>
                  </li>
                ))}
                </ul>
                )}
                </>
            )}
            </div>
        </div>
        }
        <p>{mensaje}</p>
        <button><Link to={`/wikis/${nombre}/${titulo}`}>Volver al artículo</Link></button>
        </>
        }
    </>)
}

export default VentanaHistorial;