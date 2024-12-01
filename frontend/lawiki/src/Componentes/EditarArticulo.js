import React, { useState } from "react";

const EditarArticulo = ({ nombreWiki, tituloArticulo, contenidoInicial }) => {
  const [contenido, setContenido] = useState(contenidoInicial);
  const [mensaje, setMensaje] = useState("");

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

    try {
      const response = await fetch(
        `http://127.0.0.1:8000/wikis/${nombreWiki}/articulos/${tituloArticulo}`,
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
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>Editar Artículo</h2>
      <textarea
        value={contenido}
        onChange={handleChange}
        rows="10"
        cols="50"
      />
      <button onClick={handleGuardar}>Guardar</button>
      {mensaje && <div style={{ marginTop: "10px" }}>{mensaje}</div>}
    </div>
  );
};

export default EditarArticulo;
