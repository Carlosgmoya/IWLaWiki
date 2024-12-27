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

    useEffect(() => {
        if (nombre === nombreUsuario) {
            setMiPerfil(true);
        } else {
            setMiPerfil(false);
        }
    }, [nombre, nombreUsuario]);

    useEffect(() => {
        fetch(`${backendURL}/valoracion/${nombre}`)
            .then((response) => response.json())
            .then((data) => {
                console.log("Datos Valoraciones:", data);
                setValoraciones(data);
            })
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
                    <button className="logout" onClick={handleCerrarSesion}>Cerrar sesión</button>
                </>
            ) : (
                <>
                    <h2>Perfil de {nombre}</h2>
                    <Valoraciones usuario={nombre} />
                    <div className="listaArticulos">
                        <h2>Articulos publicados</h2>
                        <p>En desarrollo...</p>
                    </div>
                </>
            )}
        </>
    );
}

export default VentanaUsuario;