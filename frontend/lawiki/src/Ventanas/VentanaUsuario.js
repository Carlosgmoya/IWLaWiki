import React, { useEffect, useState} from "react";
import { useParams } from "react-router-dom";

import Valoraciones from "../Componentes/Valoraciones";

function VentanaUsuario() {
    const backendURL = process.env.REACT_APP_BACKEND_URL;

    const { nombre } = useParams();
    const [valoraciones, setValoraciones] = useState(null);

    useEffect (() => {
        fetch(`${backendURL}/valoracion/${nombre}`)
            .then((response) => response.json())
            .then((data) => {
                console.log("Datos Valoraciones:", data);
                setValoraciones(data);
            })
    }, [nombre]);

    return (
        <div>
            <h2>Perfil de {nombre}</h2>
            
            <Valoraciones usuario={nombre} />
            <div className="listaArticulos">
                <h2>Articulos publicados</h2>
                <p>En desarrollo...</p>
            </div>
        </div>
    );
}

export default VentanaUsuario;