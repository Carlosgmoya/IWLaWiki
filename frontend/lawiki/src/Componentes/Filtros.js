import React, { useState, useEffect } from "react";

function Filtros({ minFecha, maxFecha, setMinFecha, setMaxFecha, usuario, setUsuario, nombre }) {
    useEffect(() => {
        console.log(typeof setUsuario);
    }, []);
    return (

        <div className="filtros">
            <div className="filtro">
            <label htmlFor="fechaMin">Selecciona una fecha mínima:</label>
            <input
                type="date"
                id="fechaMin"
                value={minFecha || ""}
                onChange={(e) => setMinFecha(e.target.value)}
            />
            </div>

            <div className="filtro">
            <label htmlFor="fechaMax">Selecciona una fecha máxima:</label>
            <input
                type="date"
                id="fechaMax"
                value={maxFecha || ""}
                onChange={(e) => setMaxFecha(e.target.value)}
            />
            </div>
            
            {nombre && (
                <div className="filtro">
                    <label htmlFor="fechaMax">Inserta un usuario:</label>
                    <input
                        type="text"
                        id="usuario"
                        value={usuario || ""}
                        onChange={(e) => setUsuario(e.target.value)}
                    />
                </div>
            )}


        </div>
    );
}

export default Filtros;