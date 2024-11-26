import React, { useState } from "react";

function EditorWiki({ onCancelar }) {
  const [nombre, setNombre] = useState("");
  const [descripcion, setDescripcion] = useState("");
  const [mensaje, setMensaje] = useState("");
  const [mostrarFormulario, setMostrarFormulario] = useState(true); // Estado para alternar formulario/mensaje

  const handleSubmit = async (e) => {
    e.preventDefault();

    try {
      const response = await fetch("http://127.0.0.1:8000/wikis", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ nombre, descripcion }),
      });

      if (!response.ok) {
        throw new Error("Error al crear la wiki");
      }

      const data = await response.json();

      if (data === "Ya existe una wiki con ese nombre") {
        setMensaje(data); // Muestra el mensaje de error
      } else {
        setMensaje("Wiki creada con éxito!");
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
        <form onSubmit={handleSubmit}>
          <h2>Inserta el nombre de la wiki</h2>
          <input
            type="text"
            value={nombre}
            onChange={(e) => setNombre(e.target.value)}
            required
          />
          <h2>Inserta la descripcion</h2>
          <textarea
            value={descripcion}
            onChange={(e) => setDescripcion(e.target.value)}
            required
          />
          <button type="submit">Crear</button>
          <button onClick={onCancelar} >Cancelar</button>
        </form>
      ) : (
        <div>
          <p>{mensaje}</p>
          <button onClick={handleVolver}>Volver</button>
        </div>
      )}
    </>
  );
}

export default EditorWiki;
