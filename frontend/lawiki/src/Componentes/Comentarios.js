import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { toast } from "react-toastify";
import emailjs from 'emailjs-com';

import { useSesion } from "../Login/authContext";
import { tienePermiso } from "../Login/auth";

import "../Estilos/Comentarios.css";

function Comentarios({ emailCreador }) {
  const backendURL = process.env.REACT_APP_BACKEND_URL;
  const serviceID = process.env.REACT_APP_EMAILJS_SERVICE_ID;
  const templateID = process.env.REACT_APP_EMAILJS_COMMENTS_TEMPLATE_ID;
  const userID = process.env.REACT_APP_EMAILJS_PUBLIC_KEY;

  const { nombreUsuario, rolUsuario } = useSesion();

  const { nombre } = useParams();
  const { titulo } = useParams();
  const [listaComentarios, setListaComentarios] = useState(null);
  const [comentario, setComentario] = useState("");
  const [nuevoComentario, setNuevoComentario] = useState(false);
  const [heComentado, setHeComentado] = useState(false);

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

    const fetchData = async () => {
      await fetch(`${backendURL}/wikis/${nombre}/articulos/${titulo}/comentarios`)
        .then((response) => response.json())
        .then((data) => {
          if (data["detail"] !== null) {
            setListaComentarios(data);
          }
        });

      //COMPROBAR SI HE COMENTADO
      const respuesta = await fetch(`${backendURL}/wikis/${nombre}/articulos/${titulo}/comentarios/${nombreUsuario}`);

      if (respuesta.ok) {
        setHeComentado(true);
        console.log("He comentado");
      }
    }

    fetchData();
  }, [nombre, titulo, nuevoComentario]);

  const handleInput = (event) => {
    setComentario(event.target.value);
  };

  const handleEnviarComentario = async () => {
    const datos = {
      usuario: nombreUsuario,
      contenido: comentario,
    };
    console.log("comentario: ", comentario);

    const respuesta = await fetch(`${backendURL}/wikis/${nombre}/articulos/${titulo}/comentarios`,
      {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(datos),
      }
    );

    if (respuesta.ok) {
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
    }

    const datosEmail = {
      usuario: nombreUsuario,
      mensaje: comentario,
      articulo: titulo,
      creador: emailCreador,
    };

    try {
      emailjs.send(
        serviceID,
        templateID,
        datosEmail,
        userID,
      );
    } catch (error) {
      console.log("Error enviando email con emailJS:", error);
    }
  };

  return (
    <div className="comentarios">
      <h2>Comentarios del artículo</h2>
      {
        tienePermiso(rolUsuario, "crearComentario") &&
        !heComentado &&
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
        <p className="mensajeCarga">Cargando...</p>
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
            <p className="mensajeCarga">No hay comentarios disponibles</p>
          )}
        </>
      )}
    </div>
  );
}
export default Comentarios;