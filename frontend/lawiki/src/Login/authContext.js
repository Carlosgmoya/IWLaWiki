import React, { createContext, useEffect, useContext, useState } from "react";
import { auth } from "./firebase-config";
import { signInWithGoogle, logout } from "./firebase";

const authContext = createContext();

export const useSesion = () => useContext(authContext);

export const Sesion = ({ children }) => {
    const [usuario, setUsuario] = useState(null);

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
        } catch (error) {
            console.error("Error iniciando sesion:", error.message);
        }
    };

    const cerrarSesion = async () => {
        try {
            await logout();
            setUsuario(null);
        } catch (error) {
            console.error("Error cerrando sesion:", error.message);
        }
    };

    return (
        <authContext.Provider value={{ usuario, iniciarSesion, cerrarSesion }}>
            {children}
        </authContext.Provider>
    );
};

