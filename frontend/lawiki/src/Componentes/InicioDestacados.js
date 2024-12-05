import React from "react";

function InicioDestacados({ listaWikis }) {
  return (
    <div>
      <div className="listaArticulos">
        <h2>Artículos Recientes</h2>
        <div>Futura lista de artículos recientes</div>
      </div>

      <div className="wikisDestacadas">
        <h2>Wikis Destacadas</h2>
        {listaWikis.length > 0 ? (
          <ul className="ulWikis">
            {listaWikis.map((wiki, index) => (
              <a title={"Ir a " + wiki.nombre} href={`http://localhost:3000/wikis/${wiki.nombre}`}>
                <li key={index}>
                  <p>{wiki.nombre}</p>
                  <img src="/Iconos/IconoFlecha.svg" alt={"Ir a " + wiki.nombre}></img>
                </li>
              </a>
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
