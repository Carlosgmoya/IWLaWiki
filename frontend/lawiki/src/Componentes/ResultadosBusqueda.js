import React from "react";
import { Link } from "react-router-dom";

function ResultadosBusqueda({ listaBusqueda, nombrewiki }) {
  return (
    <div className="listaWikis">

      {nombrewiki == null ? (
        <>
          <h2>Resultados de la Búsqueda</h2>
          {listaBusqueda.length > 0 ? (
            <ul className="ulWikis">
              {listaBusqueda.map((wiki, index) => (
                <Link title={"Ir a " + wiki.nombre} to={`/wikis/${wiki.nombre || 'defaultWiki'}`}>
                  <li key={index}>          
                    <p>{wiki.nombre}</p>
                    <img src="/Iconos/IconoFlecha.svg" alt={"Ir a " + wiki.nombre}></img>                 
                  </li>
                </Link>
              ))}
            </ul>
          ) : (
            <p>No se encontraron resultados.</p>
          )}
        </>
      ) : (
        <>
          <h2>Resultados de la Búsqueda</h2>
          {listaBusqueda.length > 0 ? (
            <ul className="ulArticulos">
              {listaBusqueda.map((articulo, index) => (
                <Link href={`/wikis/${nombrewiki}/articulos/${articulo.titulo || 'defaultArticulo'}`}>
                  <li key={index}>
                    <p>{articulo.titulo}</p>
                  </li>
                </Link>
              ))}
            </ul>
          ) : (
            <p>No se encontraron resultados.</p>
          )}
        </>
      )}


    </div>
  );
}

export default ResultadosBusqueda;
