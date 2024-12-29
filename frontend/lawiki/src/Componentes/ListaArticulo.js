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
    const [idioma, setIdioma] = useState("es");
    const [verIdiomas, setVerIdiomas] = useState(false);

    const listaIdiomas = [
        { code: "es", name: "Español" },
        { code: "en", name: "Inglés" },
        { code: "fr", name: "Francés" },
        { code: "de", name: "Alemán" }
      ];

    useEffect(() => {
        console.log(typeof setUsuario);
        fetchArticulos();
    }, [minFecha, maxFecha, usuario, idioma]);

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
    }, [retrasoBusqueda, minFecha, maxFecha, usuario, idioma]);

    const fetchArticulos = async () => {
        try {
            let url = `${backendURL}/wikis/${nombreWiki}/articulos`;

            const params = new URLSearchParams();

            if (minFecha) params.append("minFecha", minFecha);
            if (maxFecha) params.append("maxFecha", maxFecha);
            if (usuario != "") params.append("usuario", usuario);
            if (idioma != "") params.append("idioma", idioma);

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
            if (idioma != "") url += `&idioma=${idioma}`

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

    const handleVerIdiomas = () => {
        setVerIdiomas((anterior) => !anterior);
    };

    const handleCambiarIdioma = (code) => {
        setIdioma(code); // Cambiar el idioma
        setVerIdiomas(false); // Cerrar la lista al seleccionar un idioma
    };

    function formatearFecha(fecha) {
        console.log(fecha);
        const options = { year: 'numeric', month: 'long', day: 'numeric' }; // Example format: March 11, 2024
        return new Date(fecha).toLocaleDateString('es-ES', options); // You can change the locale if necessary
    }

    return (
        <div>

            <div className="input">
                <input
                    type="text"
                    value={terminoDeBusqueda}
                    onChange={(e) => setTerminoDeBusqueda(e.target.value)}
                    placeholder="Buscar Artículos..."
                />
                <button onClick={handleAbrirOCerrarFiltros}>
                    <img src="/Iconos/IconoFiltrar.svg" />
                </button>
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
                idioma={idioma}
                setIdioma={setIdioma}
            />
            )}

            <div className="contenedorArticulos">
                {terminoDeBusqueda === "" ? (
                    <>
                        <div className="cabeceraLista">
                            <h2>Lista Articulos</h2>
                            <div className="listaIdiomas">
                                <button onClick={handleVerIdiomas}>
                                    <img src="/Iconos/IconoIdioma.svg" alt="Cambiar idioma" />
                                    <p>Cambiar idioma</p>
                                    <img src="/Iconos/IconoDropdown.svg" alt="Desplegar lista de idiomas" />
                                </button>
                                {verIdiomas && (
                                     <ul className="ulIdiomas">
                                     {listaIdiomas.map((idiomaItem) => (
                                        <button onClick={() => handleCambiarIdioma(idiomaItem.code)}>
                                            <li key={idiomaItem.code} >
                                                {idiomaItem.name}
                                            </li>
                                        </button>
                                     ))}
                                   </ul>
                                )}
                            </div>
                        </div>
                        {listaArticulos.length > 0 ? (
                            <ul className="ulArticulos">
                                {listaArticulos.map((articulo, index) => (
                                    //<li key={index}>{listaArticulos.titulo}</li> // Asumiendo que cada wiki tiene un campo `nombre`
                                    <Link title={"Ir a " + articulo.titulo} to={`/wikis/${nombreWiki || 'defaultNombre'}/${articulo.titulo || 'defaultArticulo'}`}>
                                        <li key={index}>
                                            <h4>{articulo.titulo || "Artículo sin título"}</h4>
                                            <div className="datosArticulo">
                                                <p>lang: {articulo.idioma}</p>
                                                <p className="fecha">{formatearFecha(articulo.fecha.$date)}</p>
                                            </div>
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
                                        <h4>{articulo.titulo || "Artículo sin título"}</h4>
                                            <div className="datosArticulo">
                                                <p>lang: {articulo.idioma}</p>
                                                <p className="fecha">{formatearFecha(articulo.fecha.$date)}</p>
                                            </div>
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
