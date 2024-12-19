import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function ListaArticulo({ nombreWiki }) {

    const backendURL = process.env.REACT_APP_BACKEND_URL;

    const [listaArticulos, setListaArticulos] = useState([]);
    const [listaArticulosBusqueda, setListaArticulosBusqueda] = useState([]);
    const [terminoDeBusqueda, setTerminoDeBusqueda] = useState("");
    const [retrasoBusqueda, setRetrasoBusqueda] = useState(""); // Término con debounce.

    useEffect(() => {
        fetchArticulos();
    }, []);

    useEffect(() => {
        // Configura un debounce: espera 300ms antes de actualizar el término de búsqueda.
        const handler = setTimeout(() => {
            setRetrasoBusqueda(terminoDeBusqueda);
        }, 300);

        return () => {
            clearTimeout(handler); // Limpia el temporizador si el usuario sigue escribiendo.
        };
    }, [terminoDeBusqueda]);

    useEffect(() => {
        if (retrasoBusqueda.trim()) {
            fetchBusqueda(retrasoBusqueda);
        } else {
            setListaArticulosBusqueda([]); // Limpia los resultados si no hay término de búsqueda.
        }
    }, [retrasoBusqueda]);

    const fetchArticulos = async () => {
        try {
            const response = await fetch(`${backendURL}/wikis/${nombreWiki}/articulos`);
            const data = await response.json();
            if (Array.isArray(data)) {
                setListaArticulos(data);
            } else {
                console.error("Error: La respuesta no es una lista.");
            }
        } catch (error) {
            console.error("Error al obtener la lista de artículos:", error);
        }
    };

    const fetchBusqueda = async (term) => {
        try {
            const response = await fetch(`${backendURL}/wikis/${nombreWiki}/articulos?term=${terminoDeBusqueda}`);
            const data = await response.json();
            if (Array.isArray(data)) {
                setListaArticulosBusqueda(data); // Actualiza los resultados de búsqueda.
            } else {
                console.error("Error: La respuesta no es una lista.");
            }
        } catch (error) {
            console.error("Error al buscar articulos:", error);
        }
    };

    return (
        <div>

            <div className="input">
                <input
                    type="text"
                    value={terminoDeBusqueda}
                    onChange={(e) => setTerminoDeBusqueda(e.target.value)}
                    placeholder="Buscar Artículos..."
                />
            </div>

            <div className="contenedorArticulos">
                {terminoDeBusqueda === "" ? (
                    <>
                        <h2>Lista Articulos</h2>
                        {listaArticulos.length > 0 ? (
                            <ul className="ulArticulos">
                                {listaArticulos.map((articulo, index) => (
                                    //<li key={index}>{listaArticulos.titulo}</li> // Asumiendo que cada wiki tiene un campo `nombre`
                                    <Link title={"Ir a " + articulo.titulo} to={`/wikis/${nombreWiki || 'defaultNombre'}/${articulo.titulo || 'defaultArticulo'}`}>
                                        <li key={index}>
                                            <p>{articulo.titulo || "Artículo sin título"}</p>
                                        </li>
                                    </Link>
                                ))}
                            </ul>
                        ) : (
                            <p>No hay articulos disponibles</p>
                        )}
                    </>
                ) : (
                    <>
                        <h2>Resultados de la Búsqueda</h2>
                        {listaArticulosBusqueda.length > 0 ? (
                            <ul className="ulArticulos">
                                {listaArticulosBusqueda.map((articulo, index) => (
                                    <Link title={"Ir a " + articulo.titulo}  to={`/wikis/${nombreWiki}/articulos/${articulo.titulo || 'defaultArticulo'}`}>
                                        <li key={index}>
                                            <p>{articulo.titulo}</p>
                                            <img src="/Iconos/IconoFlecha.svg" alt={"Ir a " + articulo.titulo}></img>
                                        </li>
                                    </Link>
                                ))}
                            </ul>
                        ) : (
                            <p>No se encontraron resultados.</p>
                        )}
                    </>
                )}

            </div>
        </div>
    );
}

export default ListaArticulo;
