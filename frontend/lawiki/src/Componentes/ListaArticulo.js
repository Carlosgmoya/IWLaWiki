import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import Filtros from "./Filtros";

function ListaArticulo({ nombreWiki }) {

    const backendURL = process.env.REACT_APP_BACKEND_URL;

    const [listaArticulos, setListaArticulos] = useState([]);
    const [listaArticulosBusqueda, setListaArticulosBusqueda] = useState([]);
    const [terminoDeBusqueda, setTerminoDeBusqueda] = useState("");
    const [retrasoBusqueda, setRetrasoBusqueda] = useState(""); // Término con debounce.
    const [minFecha, setMinFecha] = useState(null);
    const [maxFecha, setMaxFecha] = useState(null);
    const [filtros, setFiltros] = useState(null);
    const [usuario, setUsuario] = useState("");   

    useEffect(() => {
        console.log(typeof setUsuario);
        fetchArticulos();
    }, [minFecha, maxFecha, usuario]);

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
    }, [retrasoBusqueda, minFecha, maxFecha, usuario]);

    const fetchArticulos = async () => {
        try {
            let url = `${backendURL}/wikis/${nombreWiki}/articulos`;

            const params = new URLSearchParams();

            if (minFecha) params.append("minFecha", minFecha);
            if (maxFecha) params.append("maxFecha", maxFecha);
            if (usuario != "") params.append("usuario", usuario);

            if (params.toString()) url += `?${params.toString()}`;

            const response = await fetch(url);  //Ahora mismo devuelve todas las wikis
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
            let url = `${backendURL}/wikis/${nombreWiki}/articulos?terminoDeBusqueda=${term}`;

            if (minFecha) url += `&minFecha=${minFecha}`;
            if (maxFecha) url += `&maxFecha=${maxFecha}`;
            if (usuario != "") url += `&usuario=${usuario}`

            const response = await fetch(url);
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

    const handleAbrirOCerrarFiltros = () => {
        // Restablece el formulario
        setFiltros(!filtros);        
        setMinFecha(null);
        setMaxFecha(null);
        setUsuario("");
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
                <button onClick={handleAbrirOCerrarFiltros}>Filtros</button>
            </div>

            {filtros && (
                <Filtros
                minFecha={minFecha}
                maxFecha={maxFecha}
                setMinFecha={(fecha) => setMinFecha(fecha)}
                setMaxFecha={(fecha) => setMaxFecha(fecha)}
                usuario={usuario}
                setUsuario={setUsuario}
                nombre={true}
            />
            )}

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
                                    <Link title={"Ir a " + articulo.titulo}  to={`/wikis/${nombreWiki}/${articulo.titulo || 'defaultArticulo'}`}>
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
