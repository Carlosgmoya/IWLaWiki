import React, { useState, useEffect } from "react";
import SubirImagen from "./SubirImagen";

function EditorWiki({ onCancelar, wiki, onWikiActualizado }) {
  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [mostrarFormulario, setMostrarFormulario] = useState(true); // Estado para alternar formulario/mensaje
  const [archivoP, setArchivoP] = useState(null);
  const [archivoC, setArchivoC] = useState(null);
  const [portada, setPortada] = useState("");
  const [cabecera, setCabecera] = useState("");
  const backendURL = process.env.REACT_APP_BACKEND_URL;
  useEffect(() => {
    console.log(wiki)

    if (wiki?.nombre) {
      setNombre(wiki.nombre);
    }
    if (wiki?.descripcion) {
      setDescripcion(wiki.descripcion);
    }
    if (wiki?.portada) {
      setPortada(wiki.portada);
    }
    if (wiki?.cabecera) {
      setCabecera(wiki.cabecera);
    }
  }, [wiki]); // Se ejecuta cuando 'wiki' cambia

  const handleArchivoP = (e) => {
    setArchivoP(e.target.files[0]);
  };

  const handleArchivoC = (e) => {
    setArchivoC(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const formData = new FormData();
    formData.append("nombre", nombre);
    formData.append("descripcion", descripcion);

    formData.append("archivoP", archivoP); // archivoP es un objeto File

    formData.append("archivoC", archivoC); // archivoC es un objeto File

    for (let pair of formData.entries()) {
      console.log(pair[0], pair[1]);
    }

    try {
      let response;

      if (wiki) {
        const data = {
          nombre: nombre,
          descripcion: descripcion,
          portada: portada,
          cabecera: cabecera,
        }
        response = await fetch(`${backendURL}/wikis/${wiki._id.$oid}`, {
          method: "PUT",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify(data),
        });
      } else {

        const formData = new FormData();
        formData.append("nombre", nombre);
        formData.append("descripcion", descripcion);

        formData.append("archivoP", archivoP); // archivoP es un objeto File

        formData.append("archivoC", archivoC); // archivoC es un objeto File

        response = await fetch(`${backendURL}/wikis`, {
          method: "POST",
          body: formData,
        });
      }

      if (response.ok) {
        const data = await response.json();
        if (wiki) {
          setMensaje("Wiki actualizada con éxito!");
        } else {
          if (data === "Ya existe una wiki con ese nombre") {
            setMensaje(data); // Muestra el mensaje de error
          } else {
            setMensaje("Wiki creada con éxito!");
          }
        }

      } else {
        const errorData = await response.json();
        console.error("Error:", errorData);
        setMensaje("Error:", errorData);
      }
    } catch (error) {
      setMensaje("Error al crear la wiki");
      console.error("Error:", error);
    } finally {
      setMostrarFormulario(false); // Cambia al mensaje después del envío
    }
  };

  const handleVolver = () => {
    // Restablece el formulario
    setMostrarFormulario(true);
    setMensaje("");
  };


  return (
    <>
      {mostrarFormulario ? (
        
        <>
        <form onSubmit={handleSubmit}>
          <h2>Título</h2>
          <input className="editorTituloWiki"
            type="text"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
          />

          <h2>Descripción</h2>
          <textarea className="editorWiki"
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            required
          />

          {wiki ? (
            <>
              <h2>Imagén Portada</h2>
              <img src={wiki.portada} alt="Imagen Portada" />
              <label>
                En caso de querer cambiar la imagen inserte la nueva url aquí:
                <input
                  className="editorTituloWiki"
                  type="text"
                  value={portada}
                  onChange={(e) => setPortada(e.target.value)}

                />
              </label>
              <h2>Imagén Cabecera</h2>
              <img src={wiki.cabecera} alt="Imagen Cabecera" />
              <label>
                En caso de querer cambiar la imagen inserte la nueva url aquí:
                <input
                  className="editorTituloWiki"
                  type="text"
                  value={cabecera}
                  onChange={(e) => setCabecera(e.target.value)}
                />
              </label>
              <div>
                <button className="botonCrear" type="submit">Actualizar</button>
                <button className="botonCancelar" onClick={onCancelar} >Cancelar</button>
              </div>
              
            </>
          ) : (
            <>
              <h2>Imagén Portada</h2>
              <label>
                En caso de querer cambiar la imagen seleccione:
                <input
                  type="file"
                  onChange={handleArchivoP}
                  required
                />
              </label>
              <h2>Imagén Cabecera</h2>
              <label>
                En caso de querer cambiar la imagen seleccione
                <input
                  type="file"
                  onChange={handleArchivoC}
                  required
                />
              </label>
              <div>
                <button className="botonCrear" type="submit">Crear</button>
                <button className="botonCancelar" onClick={onCancelar} >Cancelar</button>
              </div>
            </>
          )}
        </form>
        {wiki && (
          <>
            <SubirImagen/>
          </>
        )}
        </>
      ) : (
        <div>
          <p>{mensaje}</p>
          <button onClick={handleVolver}>Volver al editor</button>
          {wiki ? (
            <button onClick={onWikiActualizado}>Volver a la Wiki</button>)
            : (
              <button onClick={onCancelar}>Finalizar</button>
            )}

        </div>
      )}
    </>
  );
}

export default EditorWiki;
