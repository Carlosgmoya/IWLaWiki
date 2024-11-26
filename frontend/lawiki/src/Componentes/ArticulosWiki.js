import React from "react";

function ArticulosWiki({ listaArticulos, nombre}) {
  return (
    <div>
      
      <div>
        <h2>Lista Articulos</h2>
        {listaArticulos.length > 0 ? (
            <ul>
              {listaArticulos.map((articulo, index) => (
                //<li key={index}>{listaArticulos.titulo}</li> // Asumiendo que cada wiki tiene un campo `nombre`
                <li key={index}><a href={`http://localhost:3000/wikis/${nombre}/${articulo.titulo}`}>{articulo.titulo || "Artículo sin título"}</a></li>
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
