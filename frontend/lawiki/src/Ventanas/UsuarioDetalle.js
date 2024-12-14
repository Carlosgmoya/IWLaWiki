import React, { useEffect, useState} from "react";
import { useParams } from "react-router-dom";

function UsuarioDetalle() {
    const { nombre } = useParams();
    const [valoraciones, setValoraciones] = useState(null);

    useEffect (() => {
        fetch(`http://127.0.0.1:8000/valoracion/${nombre}`)
            .then((response) => response.json())
            .then((data) => {
                console.log("Datos Valoraciones:", data);
                setValoraciones(data);
            })
    }, [nombre]);

    return (
        <div>
            <h2>Perfil de {nombre}</h2>
            
            <div className="valoraciones">
                <h2>Valoraciones</h2>
                {valoraciones ? (
                    <div className="estrellasValoracion">
                        <p>{valoraciones.valor} estrellas</p>
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
            </div>
            <div className="listaArticulos">
                <h2>Articulos publicados</h2>
                <p>En desarrollo...</p>
            </div>
        </div>
    );
}

export default UsuarioDetalle;