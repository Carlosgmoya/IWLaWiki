import React from "react";

function ResultadosBusqueda({ listaBusqueda, nombrewiki }) {
  return (
    <div>

      {nombrewiki == null ? (
        <>
          <h2>Resultados de la Búsqueda</h2>
          {listaBusqueda.length > 0 ? (
            <ul>
              {listaBusqueda.map((wiki, index) => (
                <li key={index}>
                  <a href={`http://localhost:3000/wikis/${wiki.nombre}`}>
                    {wiki.nombre}
                  </a>
                </li>
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
            <ul>
              {listaBusqueda.map((articulo, index) => (
                <li key={index}>
                  <a href={`http://localhost:3000/wikis/${nombrewiki}/articulos/${articulo.titulo}`}>
                    {articulo.titulo}
                  </a>
                </li>
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
