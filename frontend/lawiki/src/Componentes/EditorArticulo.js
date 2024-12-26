import React, { useState, useRef } from "react";
import SubirMapa from "./SubirMapa";
import SubirImagen from "./SubirImagen";

const EditorArticulo = ({ nombreWiki, tituloArticulo, contenidoInicial, onCancelar }) => {
  const backendURL = process.env.REACT_APP_BACKEND_URL;

  const [contenido, setContenido] = useState(contenidoInicial);
  const [mensaje, setMensaje] = useState("");
  const [mostrarFormulario, setMostrarFormulario] = useState(true); // Estado para alternar formulario/mensaje 

  const referenciaTextArea = useRef(null);


  // Cambia esto por el ID real del creador que corresponda a tu contexto.
  const creadorId = "671fcdfdf45c1f9bfed57032";

  const handleChange = (e) => {
    setContenido(e.target.value);
  };

  const handleGuardar = async () => {
    const datos = {
      contenido,
      creador: { $oid: creadorId }, // Incluye el ID del creador en el formato requerido
    };

    //comprobar si el articulo tenia mapa y actualizar la referencia al articulo
    try {
      const respuesta = await fetch(
        `${backendURL}/wikis/${nombreWiki}/articulos/${tituloArticulo}/mapas`
      );
      
      if (respuesta.ok) {
        const mapa = respuesta.json();
        const mapaActualizado = {
          latitud: mapa.latitud,
          longitud: mapa.longitud,
          nombreUbicacion: mapa.nombreUbicacion,
        }
        const actualizar = await fetch(
          `${backendURL}/wikis/${nombreWiki}/articulos/${tituloArticulo}/mapas`,
          {
            method: "PUT",
            headers: { "Content-Type": "application/json" },
            body: mapaActualizado,
          }
        );
      }
    } catch (error) {
      console.error("Error:", error);
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
          <div className="BotonesEditor">
            <button onClick={handleTitulo}>Insertar Titulo</button>
            <button onClick={handleSubtitulo}>Insertar Subtitulo</button>
            <button onClick={handleCursiva}>Insertar Cursiva</button>
            <button onClick={handleNegrita}>Insertar Negrita</button>
            <button onClick={handleCursivayNegrita}>Insertar cursiva y negrita</button>
            <button onClick={handleEnlaceOtraPagina}>Insertar Enlace</button>
            <button onClick={handleEnlaceImagen}>Insertar Enlace Imagen</button>
            <button onClick={handleLista}>Insertar Lista</button>
          </div>


          <textarea
            ref={referenciaTextArea} // Asocia la referencia al textarea
            value={contenido}
            onChange={handleChange}
            rows="10"
            cols="50"
          />
          <button onClick={handleGuardar}>Guardar</button>
          
          <div>
            <h1>Subir Imagen</h1>
            <SubirImagen />
          </div>
          <div>
            <SubirMapa
              nombreWiki={nombreWiki}
              tituloArticulo={tituloArticulo}
            />
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
