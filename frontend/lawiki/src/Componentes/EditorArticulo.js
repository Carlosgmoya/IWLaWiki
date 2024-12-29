import React, { useState, useRef } from "react";
import emailjs from 'emailjs-com';

import SubirMapa from "./SubirMapa";
import SubirImagen from "./SubirImagen";
import { useSesion } from "../Login/authContext";

const EditorArticulo = ({ nombreWiki, tituloArticulo, contenidoInicial, emailCreador, creadorId, idioma, onCancelar }) => {
  const backendURL = process.env.REACT_APP_BACKEND_URL;
  const serviceID = process.env.REACT_APP_EMAILJS_SERVICE_ID;
  const templateID = process.env.REACT_APP_EMAILJS_ARTICLECHANGED_TEMPLATE_ID;
  const userID = process.env.REACT_APP_EMAILJS_PUBLIC_KEY;

  const { nombreUsuario } = useSesion();

  const [contenido, setContenido] = useState(contenidoInicial);
  const [mensaje, setMensaje] = useState("");
  const [mostrarFormulario, setMostrarFormulario] = useState(true); // Estado para alternar formulario/mensaje 

  const referenciaTextArea = useRef(null);


  const handleChange = (e) => {
    setContenido(e.target.value);
  };

  const handleGuardar = async () => {
    const datos = {
      contenido,
      creador: { $oid: creadorId },
      idioma
    };

    //comprobar si el articulo tenia mapa y actualizar la referencia al articulo

    const respuesta = await fetch(
      `${backendURL}/wikis/${nombreWiki}/articulos/${tituloArticulo}/mapas`
    );
    
    if (respuesta.status === 404) {
      console.log("Artículo no tiene mapa");
    } else if (respuesta.ok) {
      const mapa = respuesta.json();
      const mapaActualizado = {
        latitud: mapa.latitud,
        longitud: mapa.longitud,
        nombreUbicacion: mapa.nombreUbicacion,
      }
      try {
        const actualizar = await fetch(
          `${backendURL}/wikis/${nombreWiki}/articulos/${tituloArticulo}/mapas`,
          {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: mapaActualizado,
          }
        );
      } catch (error) {
        console.error("Error:", error);
      }
    }


    try {
      const response = await fetch(
        `${backendURL}/wikis/${nombreWiki}/articulos/${tituloArticulo}`,
        {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(datos),
        }
      );

      if (response.ok) {
        setMensaje("¡Guardado exitosamente!");

        const datosEmail = {
          usuario: nombreUsuario,
          articulo: tituloArticulo,
          creador: emailCreador,
        }

        /*emailjs.send(
          serviceID,
          templateID,
          datosEmail,
          userID,
        );*/
      } else {
        const errorData = await response.json();
        console.error("Error:", errorData);
        setMensaje("Error al guardar el artículo.");
      }
    } catch (error) {
      console.error("Error:", error);
      setMensaje("Error inesperado al conectar con el servidor.");
    }
    setMostrarFormulario(false);
  };

  const handleTitulo = async () => {
    insertarTexto("# Inserta aquí tu título");
  };

  const handleSubtitulo = async () => {
    insertarTexto("## Inserta aquí tu Subtítulo");
  };

  const handleCursiva = async () => {
    insertarTexto("*cursiva*");
  };

  const handleNegrita = async () => {
    insertarTexto("**negrita**");
  };

  const handleCursivayNegrita = async () => {
    insertarTexto("***cursiva y negrita***");
  };

  const handleEnlaceOtraPagina = async () => {
    insertarTexto("[Enlace a otra página](https://otra-pagina.com)");
  };

  const handleEnlaceImagen = async () => {
    insertarTexto("![Descripción de la imagen](url de la imagen)");
  };

  const handleLista = async () => {
    insertarTexto("- elemento de la lista");
  };



  const insertarTexto = (textoAInsertar) => {
    const textArea = referenciaTextArea.current;

    if (textArea) {
      const inicio = textArea.selectionStart;
      const final = textArea.selectionEnd;

      // Inserto el texto donde estaba el cursos
      const nuevoContenido =
        contenido.slice(0, inicio) +
        textoAInsertar +
        contenido.slice(final);

      setContenido(nuevoContenido);

      // Actualizo la posicion del cursor
      setTimeout(() => {
        textArea.setSelectionRange(
          inicio + textoAInsertar.length,
          inicio + textoAInsertar.length
        );
      }, 0);
    }
  };



  return (
    <>
      {mostrarFormulario ? (
        <div style={{ padding: "20px" }}>
          <h2>Editar Artículo</h2>
          <div className="botonesEditor">
            <button onClick={handleTitulo}>Insertar Titulo</button>
            <button onClick={handleSubtitulo}>Insertar Subtitulo</button>
            <button onClick={handleCursiva}>Insertar Cursiva</button>
            <button onClick={handleNegrita}>Insertar Negrita</button>
            <button onClick={handleCursivayNegrita}>Insertar cursiva y negrita</button>
            <button onClick={handleEnlaceOtraPagina}>Insertar Enlace</button>
            <button onClick={handleEnlaceImagen}>Insertar Enlace Imagen</button>
            <button onClick={handleLista}>Insertar Lista</button>
          </div>

          <div className="contenedorEditarArticulo">
            <textarea
              className="editarArticulo"
              ref={referenciaTextArea} // Asocia la referencia al textarea
              value={contenido}
              onChange={handleChange}
              rows="20"
              cols="200"
            />
          </div>
          
          <SubirImagen />
          
          <SubirMapa
            nombreWiki={nombreWiki}
            tituloArticulo={tituloArticulo}
          />

          <div className="contenedorBotonesGuardar">
            <button className="botonGuardar" onClick={handleGuardar}>Guardar</button>
            <button className="botonCancelar" onClick={onCancelar}>Cancelar</button>
          </div>
        </div>
      ) : (
        <>
          {mensaje && <div style={{ marginTop: "10px" }}>{mensaje}</div>}
        </>
      )}
    </>
  );
};

export default EditorArticulo;
