import React, { useEffect, useState } from "react";
import { toast } from "react-toastify";

import { useSesion } from "../Login/authContext";
import { tienePermiso } from "../Login/auth";

function Valoraciones({ usuario }) {
    const backendURL = process.env.REACT_APP_BACKEND_URL;

    const { nombreUsuario, rolUsuario } = useSesion();

    const [valoraciones, setValoraciones] = useState(null);
    const [mostrarValorar, setMostrarValorar] = useState(false);
    const [puntuacion, setPuntuacion] = useState(0);
    const [puntuacionSeleccionada, setPuntuacionSeleccionada] = useState(0);
    const [nuevaValoracion, setNuevaValoracion] = useState(false);

    useEffect(() => {
        if (nuevaValoracion) {
            console.log("Nueva valoracion añadida");
            setNuevaValoracion(false);
        }
        fetch(`${backendURL}/valoracion/${usuario}`)
            .then((response) => response.json())
            .then((data) => {
                console.log("Datos Valoraciones:", data);
                setValoraciones(data);
            })
    }, [usuario, nuevaValoracion]);

    const handleAbrirValorar = () => {
        setMostrarValorar(true);
    };

    const handleCerrarValorar = () => {
        setMostrarValorar(false);
    };

    const handlePuntuar = (estrellas) => {
        console.log(`Clickeado boton ${estrellas}`);
        if (puntuacionSeleccionada === estrellas) {
            setPuntuacion(0);
            setPuntuacionSeleccionada(0);
        } else {
            setPuntuacion(estrellas);
            setPuntuacionSeleccionada(estrellas);
        }
    };

    const handleConfirmarPuntuacion = () => {
        const datos = {
            de_usuario: nombreUsuario,
            a_usuario: usuario,
            valor: puntuacion,
        };

        fetch(`${backendURL}/valoraciones`,
            {
                method: "POST",
                headers: { "Content-Type": "application/json" },
                body: JSON.stringify(datos),
            }
        );

        setMostrarValorar(false);
        setNuevaValoracion(true);

        toast.success("Valoración enviada con éxito", {
            position: "top-right",
            autoClose: 3000, // Auto close after 3 seconds
            hideProgressBar: false,
            closeOnClick: true,
            pauseOnHover: true,
            draggable: true,
            progress: undefined,
        });
    };

    return (
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
            {tienePermiso(rolUsuario, "crearValoracion") &&
                <>
                    <button onClick={handleAbrirValorar}>Valorar a {usuario}</button>
                    {mostrarValorar && 
                        <div className="valorar">
                            <h3>Hola {nombreUsuario}! Puntúa a {usuario}</h3>
                            {Array.from({ length: 5 }).map((_, index) => (
                                <button
                                    key={index + 1}
                                    onClick={() => handlePuntuar(index + 1)}
                                >
                                    {index >= puntuacion ? (
                                        <img src="/Iconos/Estrella3.png" alt="Estrella vacia" />
                                        ) : (
                                        <img src="/Iconos/Estrella1.png" alt="Estrella" />
                                    )}
                                </button>
                            ))}
                            <textarea className="reseña"
                                type="text"
                                placeholder="Comparte tu crítica constructiva del usuario"
                            />
                            <button onClick={handleConfirmarPuntuacion}>Confirmar</button>
                            <button onClick={handleCerrarValorar}>Cancelar</button>
                        </div>
                    }
                </>
            }
        </div>
    );
}

export default Valoraciones;