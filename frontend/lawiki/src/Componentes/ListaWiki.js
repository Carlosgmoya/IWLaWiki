import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Filtros from "./Filtros";

function ListaWiki() {

    const backendURL = process.env.REACT_APP_BACKEND_URL;

    const [listaWikis, setListaWikis] = useState([]);
    const [listaWikisBusqueda, setListaWikisBusqueda] = useState([]);
    const [terminoDeBusqueda, setTerminoDeBusqueda] = useState("");
    const [retrasoBusqueda, setRetrasoBusqueda] = useState(""); // Término con debounce.
    const [minFecha, setMinFecha] = useState(null);
    const [maxFecha, setMaxFecha] = useState(null);
    const [filtros, setFiltros] = useState(null);

    useEffect(() => {
        fetchWikisDestacadas();
    }, [minFecha, maxFecha
    ]);

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
    }, [retrasoBusqueda, minFecha, maxFecha]);

    const fetchWikisDestacadas = async () => {
        try {
            let url = `${backendURL}/wikis`;

            const params = new URLSearchParams();

            if (minFecha) params.append("minFecha", minFecha);
            if (maxFecha) params.append("maxFecha", maxFecha);

            if (params.toString()) url += `?${params.toString()}`;

            const response = await fetch(url);  //Ahora mismo devuelve todas las wikis
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
            let url = `${backendURL}/wikis?term=${term}`;

            if (minFecha) url += `&minFecha=${minFecha}`;
            if (maxFecha) url += `&maxFecha=${maxFecha}`;

            const response = await fetch(url);
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

    const handleAbrirOCerrarFiltros = () => {
        // Restablece el formulario
        setFiltros(!filtros);        
        setMinFecha(null);
        setMaxFecha(null);
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
                <button onClick={handleAbrirOCerrarFiltros}>Filtros</button>

            </div>

            {filtros && (
                <Filtros
                minFecha={minFecha}
                maxFecha={maxFecha}
                setMinFecha={(fecha) => setMinFecha(fecha)}
                setMaxFecha={(fecha) => setMaxFecha(fecha)}
            />
            )}

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
                                        <li key={index} style={{ backgroundImage: `url(${wiki.portada})`, }}>
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
