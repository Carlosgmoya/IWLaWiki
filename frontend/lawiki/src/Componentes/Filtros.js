import React from "react";

function Filtros({ minFecha, maxFecha, setMinFecha, setMaxFecha }) {
    return (
        <div className="filtros">
            <label htmlFor="fechaMin">Selecciona una fecha mínima:</label>
            <input
                type="date"
                id="fechaMin"
                value={minFecha || ""}
                onChange={(e) => setMinFecha(e.target.value)} // Usa setMinFecha aquí.
            />

            <label htmlFor="fechaMax">Selecciona una fecha máxima:</label>
            <input
                type="date"
                id="fechaMax"
                value={maxFecha || ""}
                onChange={(e) => setMaxFecha(e.target.value)} // Usa setMaxFecha aquí.
            />
        </div>
    );
}

export default Filtros;