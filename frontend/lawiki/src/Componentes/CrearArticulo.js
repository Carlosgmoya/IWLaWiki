import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useSesion } from "../Login/authContext";

const CrearArticulo = ({ nombreWiki, onCancelar }) => {
    const backendURL = process.env.REACT_APP_BACKEND_URL;

    const [contenido, setContenido] = useState("");
    const [mensaje, setMensaje] = useState("");
    const [titulo, setTitulo] = useState("");
    const [mostrarFormulario, setMostrarFormulario] = useState(true); // Estado para alternar formulario/mensaje
    const [mostrarFormularioIdiomas, setMostrarFormularioIdiomas] = useState(false);
    const navigate = useNavigate();

    const [listaIdiomas, setListaIdiomas] = useState({});
    const [idioma, setIdioma] = useState("");

    const { nombreUsuario } = useSesion();

    const getCreadorId = async() => {
        const creador = await fetch(`${backendURL}/usuarios/nombre/${nombreUsuario}`);
        const creadorJson = await creador.json();
        return creadorJson._id;
    }

    const handleSubmit = async (e) => {
        e.preventDefault();
        const datos = {
            titulo,
            contenido,
            creador: await getCreadorId(),
            idioma: "es"
        };

        try {
            const response = await fetch(
                `${backendURL}/wikis/${nombreWiki}/articulos`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datos),
                }
            );
            const data = await response.json();

            if (data === "Ya existe un articulo con ese nombre") {
                setMensaje(data); // Muestra el mensaje de error
            } else {
                setMensaje("¡Articulo creado exitosamente!");
            }
        } catch (error) {
            console.error("Error:", error);
            setMensaje("Error inesperado al conectar con el servidor.");
        } finally {
            setMostrarFormulario(false); // Cambia al mensaje después del envío
            setMostrarFormularioIdiomas(true);
        }
    };

    const traducir = async(idioma) => {
        try {
            const response = await fetch(`${backendURL}/wikis/${nombreWiki}/articulos/${titulo}/traducir?idioma=${idioma}`, {
                method: "PUT"
            });
            const respuestaJson = await response.json();
            return respuestaJson;
        } catch (error) {
            console.error("Error al obtener datos:", error);
        }
    }

    const handleSubmit2 = async(e) => {
        e.preventDefault();

        try {
            const data = await traducir(idioma);
            console.log(data);

            if (data.detail != null) {
                setMensaje("No se ha podido traducir el artículo."); // Muestra el mensaje de error
            } else {
                setMensaje("¡Articulo traducido exitosamente!");
            }
        } catch (error) {
            console.error("Error:", error);
            setMensaje("Error inesperado al conectar con el servidor.");
        }
    }

    useEffect(() => {
        setListaIdiomas([
            {"code": "es", "name": "Español"},
            {"code": "en", "name": "Inglés"},
            {"code": "fr", "name": "Francés"},
            {"code": "de", "name": "Alemán"}
        ])
    }, [])

    const handleVolver = () => {
        // Restablece el formulario
        setMostrarFormulario(true);
        setMensaje("");
    };

    const handleVerArticulo = () => {
        // Construye la URL dinámica
        navigate(`/wikis/${nombreWiki}/${titulo}`);
    };

    const handleVolverWiki = () => {
        // Construye la URL dinámica
        window.location.reload();
    };

    return (
        <>
            {mostrarFormulario ? (
                <div>
                    <h2>Crear Artículo</h2>
                    <form onSubmit={handleSubmit}>
                        <h2>Inserta el titulo</h2>
                        <input type="text"
                            value={titulo}
                            onChange={(e) => setTitulo(e.target.value)} />
                        <h2>Inserta el contenido</h2>

                        <textarea
                            value={contenido}
                            onChange={(e) => setContenido(e.target.value)}
                            rows="10"
                            cols="50"
                        />
                        <button type="submit">Guardar</button>
                        <button onClick={onCancelar} >Cancelar</button>
                    </form>
                </div>
            ) : (
                <div>
                    {mensaje === "Ya existe un articulo con ese nombre" ? (
                        <>
                            <p>{mensaje}</p>
                            <button onClick={handleVolver}>Volver</button>
                        </>
                    ) : (
                        <>
                            <p>{mensaje}</p>
                            {mostrarFormularioIdiomas &&
                            <form onSubmit={handleSubmit2}>
                                <label for="idioma">Seleccione idioma:</label>
                                <select
                                    id="idioma"
                                    value={idioma}
                                    onChange={(e) => setIdioma(e.target.value)}
                                >
                                    <option value=""></option>
                                    {listaIdiomas.map((idioma) => (
                                    <option key={idioma.code} value={idioma.code}>
                                        {idioma.name}
                                    </option>
                                    ))
                                    }
                                </select>
                                <button type="submit">Traducir</button>
                                <button onClick={handleVolverWiki}>Omitir</button>
                            </form>
                            }
                            <button onClick={handleVerArticulo}>Ver Articulo</button>
                            <button onClick={handleVolverWiki}>Volver</button>
                        </>
                    )}
                </div>
            )}
        </>
    );
};

export default CrearArticulo;
