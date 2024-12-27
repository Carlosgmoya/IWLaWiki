import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";

import { useSesion } from "../Login/authContext";
import { tienePermiso } from "../Login/auth";

import "../Estilos/VentanaComentario.css";

function Comentarios() {
  const backendURL = process.env.REACT_APP_BACKEND_URL;

  const { nombreUsuario, rolUsuario } = useSesion();

  const { nombre } = useParams();
  const { titulo } = useParams();
  const [listaComentarios, setListaComentarios] = useState(null);
  const [comentario, setComentario] = useState("");
  const [nuevoComentario, setNuevoComentario] = useState(false);

  const options = {
    year: "numeric",
    month: "long",
    day: "numeric"
  };

  useEffect(() => {
    if (nuevoComentario) {
      console.log("Nuevo comentario añadido");
      setNuevoComentario(false);
    }
    fetch(`${backendURL}/wikis/${nombre}/articulos/${titulo}/comentarios`)
    .then((response) => response.json())
    .then((data) => {
      if(data["detail"] !== null) {
        setListaComentarios(data);
      }
    })
  }, [nombre, titulo, nuevoComentario]);

  const handleInput = (event) => {
    setComentario(event.target.value);
  };

  const handleEnviarComentario = () => {
    const datos = {
      usuario: nombreUsuario,
      contenido: comentario,
    };
    console.log("comentario: ", comentario);

    fetch(`${backendURL}/wikis/${nombre}/articulos/${titulo}/comentarios`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json"},
        body: JSON.stringify(datos),
      }
    );

    console.log("Comentario enviado por:", nombreUsuario);
    setNuevoComentario(true);
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
        {
        tienePermiso(rolUsuario, "crearComentario") &&
        <div className="contenedorComentar">
          <textarea className="escribirComentario"
            type="text"
            value={comentario}
            onChange={handleInput}
            placeholder="Escribe un comentario"
          />
          <button className="botonComentar" onClick={handleEnviarComentario}>
            <img src="/Iconos/IconoEnviar.svg" alt="Enviar comentario" />
          </button>
        </div>
        }
        {listaComentarios === null ? (
          <p>Cargando...</p>
        ) : (
          <>
            {listaComentarios.length > 0 ? (
            <ul>
              {listaComentarios.map((comentario, index) => (
                <li key={index}>
                  <h3>{comentario["usuario"]}</h3>
                  <h4>{new Date(comentario["fecha"]).toLocaleDateString("es-ES", options)}, {new Date(comentario["fecha"]).toLocaleTimeString("es-ES")}</h4>
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
export default Comentarios;