import React from "react";

function ArticulosWiki({ listaArticulos, nombre}) {
  return (
    <div>
      
      <div>
        <h2>Lista Articulos</h2>
        {listaArticulos.length > 0 ? (
            <ul className="ulArticulos">
              {listaArticulos.map((articulo, index) => (
                //<li key={index}>{listaArticulos.titulo}</li> // Asumiendo que cada wiki tiene un campo `nombre`
                <a href={`http://localhost:3000/wikis/${nombre}/${articulo.titulo}`}>
                  <li key={index}>
                    <p>{articulo.titulo || "Artículo sin título"}</p>
                  </li>
                </a>
              ))}
            </ul>
          ) : (
            <p>No hay articulos disponibles</p>
          )}
      </div>
    </div>
  );
}

export default ArticulosWiki;
