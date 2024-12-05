import React from "react";

function ResultadosBusqueda({ listaBusqueda, nombrewiki }) {
  return (
    <div className="listaWikis">

      {nombrewiki == null ? (
        <>
          <h2>Resultados de la Búsqueda</h2>
          {listaBusqueda.length > 0 ? (
            <ul className="ulWikis">
              {listaBusqueda.map((wiki, index) => (
                <a title={"Ir a " + wiki.nombre} href={`http://localhost:3000/wikis/${wiki.nombre}`}>
                  <li key={index}>          
                    <p>{wiki.nombre}</p>
                    <img src="/Iconos/IconoFlecha.svg" alt={"Ir a " + wiki.nombre}></img>                 
                  </li>
                </a>
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
                <a href={`http://localhost:3000/wikis/${nombrewiki}/articulos/${articulo.titulo}`}>
                  <li key={index}>
                    <p>{articulo.titulo}</p>
                  </li>
                </a>
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
