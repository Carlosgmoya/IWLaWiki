import React from "react";

function InicioDestacados({ listaWikis }) {
  return (
    <div>
      <div>
        <h2>Artículos Recientes</h2>
        <div>Futura lista de artículos recientes</div>
      </div>

      <div>
        <h2>Wikis Destacadas</h2>
        {listaWikis.length > 0 ? (
          <ul>
            {listaWikis.map((wiki, index) => (
              <li key={index}>
                <a href={`http://localhost:3000/wikis/${wiki.nombre}`}>
                  {wiki.nombre}
                </a>
              </li>
            ))}
          </ul>
        ) : (
          <p>No hay wikis disponibles</p>
        )}
      </div>
    </div>
  );
}

export default InicioDestacados;
