import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useSesion } from "../Login/authContext";

const CrearArticulo = ({ nombreWiki, onCancelar }) => {
    const backendURL = process.env.REACT_APP_BACKEND_URL;

    const [contenido, setContenido] = useState("");
    const [mensaje, setMensaje] = useState("");
    const [titulo, setTitulo] = useState("");
    const [mostrarFormulario, setMostrarFormulario] = useState(true); // Estado para alternar formulario/mensaje
    const navigate = useNavigate();

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
        };

        try {
            const response = await fetch(
                `http://localhost:8000/wikis/${nombreWiki}/articulos`,
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
        }
    };

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
