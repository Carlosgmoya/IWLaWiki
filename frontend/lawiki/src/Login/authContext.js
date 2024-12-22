import React, { createContext, useEffect, useContext, useState } from "react";
import Modal from "./Modal";
import { auth } from "./firebase-config";
import { signInWithGoogle, logout } from "./firebase";
import { toast } from "react-toastify";

const authContext = createContext();

export const useSesion = () => useContext(authContext);

const backendURL = process.env.REACT_APP_BACKEND_URL;

export const Sesion = ({ children }) => {
    const [usuario, setUsuario] = useState(null);
    const [nuevoUsuario, setNuevoUsuario] = useState(false);
    const [nombreUsuario, setNombreUsuario] = useState("");
    
    useEffect(() => {
        const sesion = auth.onAuthStateChanged((usuario) => {
            setUsuario(usuario);    // usuario actual o null
        });
        return () => sesion();
      }, []);

    const iniciarSesion = async () => {
        try {
            const u = await signInWithGoogle();
            setUsuario(u);

            //Comprobar si el usuario esta registrado en la base de datos
            const respuesta = await fetch(`${backendURL}/usuarios/email/${u.email}`);
            if (respuesta.status === 404) {
                //Crear un usuario si no esta
                console.log("Usuario no encontrado");
                setNuevoUsuario(true);
            } else {
                //Buscar el nombre de usuario si esta
                const datosUsuario = await respuesta.json();
                console.log("Iniciado sesion como:", datosUsuario["nombre"]);
                setNombreUsuario(datosUsuario["nombre"]);
            }

        } catch (error) {
            console.error("Error iniciando sesion:", error.message);
        }
    };

    const registrarUsuario = async () => {
        const datos = {
            nombre: nombreUsuario,
            email: usuario.email
        }
        console.log("Registrando usuario:", usuario.email, " con nombre:", nombreUsuario);
        
        try {
            const respuesta = await fetch(
                `${backendURL}/usuarios`,
                {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(datos),
                }
            );
            if (respuesta.ok) {
                toast.success(`Bienvenido a laWiki ${nombreUsuario}`, {
                    position: "top-right",
                    autoClose: 3000, // Auto close after 3 seconds
                    hideProgressBar: false,
                    closeOnClick: true,
                    pauseOnHover: true,
                    draggable: true,
                    progress: undefined,
                });
                setNuevoUsuario(false);
            } else {
                console.error("Error registrando usuario:", respuesta.status);
            }
        } catch (error) {
            console.error("Error registrando usuario:", error.message);
        }
    };

    const cerrarSesion = async () => {
        try {
            await logout();
            setUsuario(null);
            setNombreUsuario("");
            setNuevoUsuario(false);
        } catch (error) {
            console.error("Error cerrando sesion:", error.message);
        }
    };

    return (
        <authContext.Provider value={{ usuario, nombreUsuario, iniciarSesion, cerrarSesion }}>
            {children}
            
            {nuevoUsuario && (
                <Modal onClose={cerrarSesion}>
                    <h2>Registro de Usuario</h2>
                    <p>
                        Hemos detectado que es la primera vez que te conectas
                        a laWiki, por favor introduce un nombre de usuario para
                        identificarte
                    </p>
                    <input
                        type="text"
                        placeholder="Introduzca un nombre de usuario"
                        value={nombreUsuario}
                        onChange={(e) => setNombreUsuario(e.target.value)}
                    />
                    <div className="contenedorBotones">
                        <button className="botonRegistrar" onClick={registrarUsuario}>Registrar usuario</button>
                        <button className="botonNoRegistrar" onClick={cerrarSesion}>No quiero registrarme</button>
                    </div>
                </Modal>
            )}
        </authContext.Provider>
    );
};

