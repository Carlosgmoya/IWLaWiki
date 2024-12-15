import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";

import "../Estilos/Comentarios.css";

function ComentariosArticulo() {
  const { nombre } = useParams();
  const { titulo } = useParams();
  const [listaComentarios, setListaComentarios] = useState(null);
  const [comentario, setComentario] = useState("");

  const options = {
    year: "numeric",
    month: "long",
    day: "numeric"
  };

  useEffect(() => {
    fetch(`http://lawiki-gateway:8000/wikis/${nombre}/articulos/${titulo}/comentarios`)
    .then((response) => response.json())
    .then((data) => {
      if(data["detail"] !== null) {
        setListaComentarios(data);
      }
    })
  }, [nombre, titulo]);

  const handleInput = (event) => {
    setComentario(event.target.value);
  };

  const handleEnviarComentario = () => {
    const datos = {
      usuario: "Pepe",  //Provisional antes de implementar autenticacion
      contenido: comentario,
    };
    console.log("comentario: ", comentario);

    fetch(`http://lawiki-gateway:8000/wikis/${nombre}/articulos/${titulo}/comentarios`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(datos),
      }
    );

    toast.success("Comentario enviado con éxito", {
                position: "top-right",
                autoClose: 3000, // Auto close after 3 seconds
                hideProgressBar: false,
                closeOnClick: true,
                pauseOnHover: true,
                draggable: true,
                progress: undefined,
              });
  };

  return (
      <div className="comentarios">
        <h2>Comentarios del artículo</h2>
        <textarea className="escribirComentario"
          type="text"
          value={comentario}
          onChange={handleInput}
          placeholder="Escribe un comentario"
        />
        <button className="botonComentar" onClick={handleEnviarComentario}>
          <img src="/Iconos/IconoEnviar.svg" alt="Enviar comentario" />
        </button>
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