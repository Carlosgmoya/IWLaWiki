import React from "react";
import { Link } from "react-router-dom";

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
              <Link title={"Ir a " + wiki.nombre} to={`/wikis/${wiki.nombre || 'defaultWiki'}`}>
                <li key={index}>
                  <p>{wiki.nombre}</p>
                  <img src="/Iconos/IconoFlecha.svg" alt={"Ir a " + wiki.nombre}></img>
                </li>
              </Link>
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
