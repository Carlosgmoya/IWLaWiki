import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import "../Estilos/Comentarios.css";

function ComentariosArticulo() {
  const { nombre } = useParams();
  const { titulo } = useParams();
  const [listaComentarios, setListaComentarios] = useState(null);
  const options = {
    year: "numeric",
    month: "long",
    day: "numeric"
  };

  useEffect(() => {
    fetch(`http://127.0.0.1:8000/wikis/${nombre}/articulos/${titulo}/comentarios`)
    .then((response) => response.json())
    .then((data) => {
      if(data["detail"] !== null) {
        setListaComentarios(data);
      }
    })
  }, [nombre, titulo])

  return (
      <div className="comentarios">
        <h2>Comentarios del artículo</h2>
        {listaComentarios === null ? (
          <p>Cargando...</p>
        ) : (
          <>
            {listaComentarios.length > 0 ? (
            <ul>
              {listaComentarios.map((comentario, index) => (
                <li key={index}>
                  <h3>{new Date(comentario["fecha"]).toLocaleDateString("es-ES", options)}, {new Date(comentario["fecha"]).toLocaleTimeString("es-ES")}</h3>
                  <p>{comentario["contenido"] || ""}</p>
                </li>
              ))}
            </ul>
          ) : (
            <p>No hay comentarios disponibles</p>
          )}
          </>
        )}
      </div>
  );
}
export default ComentariosArticulo;