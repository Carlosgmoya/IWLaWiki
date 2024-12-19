import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

function ListaWiki() {

    const backendURL = process.env.REACT_APP_BACKEND_URL;

    const [listaWikis, setListaWikis] = useState([]);
    const [listaWikisBusqueda, setListaWikisBusqueda] = useState([]);
    const [terminoDeBusqueda, setTerminoDeBusqueda] = useState("");
    const [retrasoBusqueda, setRetrasoBusqueda] = useState(""); // Término con debounce.

    useEffect(() => {
        fetchWikisDestacadas();
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
            setListaWikisBusqueda([]); // Limpia los resultados si no hay término de búsqueda.
        }
    }, [retrasoBusqueda]);

    const fetchWikisDestacadas = async () => {
        try {
          const response = await fetch(`${backendURL}/wikis`);  //Ahora mismo devuelve todas las wikis
          const data = await response.json();
          if (Array.isArray(data)) {
            setListaWikis(data); // Carga las wikis destacadas.
          } else {
            console.error("Error: La respuesta no es una lista.");
          }
        } catch (error) {
          console.error("Error al obtener las wikis destacadas:", error);
        }
    };

    const fetchBusqueda = async (term) => {
        try {
            const response = await fetch(`${backendURL}/wikis?term=${term}`);
            const data = await response.json();
            if (Array.isArray(data)) {
                setListaWikisBusqueda(data); // Actualiza los resultados de búsqueda.
            } else {
                console.error("Error: La respuesta no es una lista.");
            }
        } catch (error) {
            console.error("Error al buscar wikis:", error);
        }
    };


    return (
        <div>
            <div className="input">
                <input
                    type="text"
                    value={terminoDeBusqueda}
                    onChange={(e) => setTerminoDeBusqueda(e.target.value)}
                    placeholder=" Buscar wikis..."
                />
            </div>


            <div className="listaArticulos">
                <h2>Artículos Recientes</h2>
                <div>Futura lista de artículos recientes</div>
            </div>

            <div className="contenedorWikis">
                {terminoDeBusqueda === "" ? (
                    <>
                        <h2>Wikis Destacadas</h2>
                        {listaWikis.length > 0 ? (
                            <ul className="ulWikis">
                                {listaWikis.map((wiki, index) => (
                                    <Link title={"Ir a " + wiki.nombre} to={`/wikis/${wiki.nombre || 'defaultWiki'}`}>
                                        <li key={index}>
                                            <p>{wiki.nombre}</p>
                                            <img src="/Iconos/IconoFlecha.svg" alt={"Ir a " + wiki.nombre}></img>
                                        </li>
                                    </Link>
                                ))}
                            </ul>
                        ) : (
                            <p>No hay wikis disponibles</p>
                        )}
                    </>
                ) : (
                    <>
                        <h2>Resultados de la Búsqueda</h2>
                        {listaWikisBusqueda.length > 0 ? (
                            <ul className="ulWikis">
                                {listaWikisBusqueda.map((wiki, index) => (
                                    <Link title={"Ir a " + wiki.nombre} to={`/wikis/${wiki.nombre || 'defaultWiki'}`}>
                                        <li key={index}>
                                            <p>{wiki.nombre}</p>
                                            <img src="/Iconos/IconoFlecha.svg" alt={"Ir a " + wiki.nombre}></img>
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

export default ListaWiki;
