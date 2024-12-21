import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useSesion } from '../Login/authContext';
import '../Estilos/Cabecera.css';

function Cabecera() {
    const { usuario, iniciarSesion, cerrarSesion } = useSesion();

    return <header className="contenedorCabecera">
        <h1><Link className="lawiki" to='/' reloadDocument>laWiki</Link></h1>
        {usuario ? (
            <div>
                <img className="iconoPerfil" src={usuario.photoURL} alt={usuario.display_name} />
                <button className="logout" onClick={cerrarSesion}>Cerrar sesión</button>
            </div>
        ) : (
            <>
                <button className="login" onClick={iniciarSesion}>Iniciar sesión</button>
            </>
        )}
    </header>;
}

export default Cabecera;