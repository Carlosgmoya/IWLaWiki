import React, { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import { useSesion } from "../Login/authContext";

import Valoraciones from "../Componentes/Valoraciones";

import "../Estilos/VentanaUsuario.css";

function VentanaUsuario() {
    const backendURL = process.env.REACT_APP_BACKEND_URL;
    const navigate = useNavigate();

    const { nombre } = useParams();
    const { nombreUsuario, cerrarSesion } = useSesion();

    const [miPerfil, setMiPerfil] = useState(false);
    const [valoraciones, setValoraciones] = useState(null);
    const [wikiPuntos, setWikiPuntos] = useState(null);

    useEffect(() => {
        if (nombre === nombreUsuario) {
            setMiPerfil(true);
        } else {
            setMiPerfil(false);
        }
    }, [nombre, nombreUsuario]);

    useEffect(() => {
        fetch(`${backendURL}/valoracion/${nombre}`)
            .then((respuesta) => respuesta.json())
            .then((data) => {
                console.log("Datos Valoraciones:", data);
                setValoraciones(data);
            });

        fetch(`${backendURL}/valoraciontotal/${nombre}`)
            .then((respuesta) => respuesta.json())
            .then((data) => {
                console.log("wikiPuntos:", data);
                setWikiPuntos(data);
            });  
    }, [nombre]);

    const handleCerrarSesion = () => {
        cerrarSesion();
        navigate(-1);
    }

    return (
        <>
            {miPerfil ? (
                <>
                    <h2>Mi perfil</h2>
                    <div className="valoraciones">
                        <h3>Tus wikiPuntos: {wikiPuntos && <>{wikiPuntos.valor}</>}</h3>
                        <p></p>
                        {valoraciones ? (
                            <div className="estrellasValoracion">
                                {Array.from({ length: valoraciones.valor }).map((_, index) => (
                                    <img
                                        key={index}
                                        src="/Iconos/Estrella1.png"
                                        alt={'Estrella'}
                                    />
                                ))}
                                {valoraciones.valor % 1 >= 0.5 && <img src="/Iconos/Estrella2.png" alt="Media Estrella" />}
                                {Array.from({ length: (5 - valoraciones.valor) }).map((_, index) => (
                                    <img
                                        key={index}
                                        src="/Iconos/Estrella3.png"
                                        alt={'Estrella'}
                                    />
                                ))}
                            </div>
                        ) : (
                            <p>Cargando valoraciones...</p>
                        )}
                        <p>
                            Mantén al día tus artículos, contribuye a laWiki y a su comunidad
                            para obtener más wikiPuntos.
                        </p>
                    </div>
                    <div className="contenedorLogout">
                        <button className="logout" onClick={handleCerrarSesion}>Cerrar sesión</button>
                    </div>
                </>
            ) : (
                <>
                    <h2 className="cabeceraPerfil">Perfil de {nombre}</h2>
                    <Valoraciones usuario={nombre} wikiPuntos={wikiPuntos} />
                    <div className="listaArticulos">
                        <h2>Articulos publicados</h2>
                        <p>En desarrollo... GET ARTICULOS DE UN USUARIO</p>
                    </div>
                </>
            )}
        </>
    );
}

export default VentanaUsuario;