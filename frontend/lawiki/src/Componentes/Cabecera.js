import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { useSesion } from '../Login/authContext';
import '../Estilos/Cabecera.css';

function Cabecera() {
    const { usuario, nombreUsuario, iniciarSesion } = useSesion();

    const iconoPerfilPredeterminado = "Iconos/IconoEditarPerfil.svg";

    return <header className="contenedorCabecera">
        <h1><Link className="lawiki" to='/'>laWiki</Link></h1>
        {usuario ? (
            <div>
                <Link title="Ir a mi perfil" to={`/usuario/${nombreUsuario}`}>
                    <img className="iconoPerfil" src={usuario.photoURL || iconoPerfilPredeterminado} alt={usuario.display_name} />
                </Link>
            </div>
        ) : (
            <>
                <button className="login" onClick={iniciarSesion}>Iniciar sesión</button>
            </>
        )}
    </header>;
}

export default Cabecera;