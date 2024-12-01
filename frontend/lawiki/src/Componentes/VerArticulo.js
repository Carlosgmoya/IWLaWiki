import React from "react";

const VerArticulo = ({ contenido_html }) => {
  if (!contenido_html) {
    return <div>No hay contenido para mostrar.</div>;
  }

  if (!contenido_html) {
    return <div>No hay contenido para mostrar.</div>;
  }

  return (

    
    <div
      dangerouslySetInnerHTML={{ __html: contenido_html }}
      style={{ padding: "20px", fontFamily: "Arial, sans-serif" }}
    />
  );
};

export default VerArticulo;
