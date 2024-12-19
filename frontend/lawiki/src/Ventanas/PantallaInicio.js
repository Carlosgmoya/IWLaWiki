import React, {  useState } from "react";
import '../Estilos/PantallaInicio.css';
import EditorWiki from "../Componentes/EditorWiki";
import ListaWiki from "../Componentes/ListaWiki";

function PantallaInicio() {
  
  const [mostrarCrearWiki, setMostrarCrearWiki] = useState(false);

  const handleAbrirEditor = () => {
    setMostrarCrearWiki(true); // Muestra el editor
  };

  const handleCerrarEditor = () => {
    // Restablece el formulario
    setMostrarCrearWiki(false);
  };

  return (
    <>
      {!mostrarCrearWiki ? (
        <>
        <ListaWiki/ >

            <form>
              <button className="botonIrACrearWiki" onClick={handleAbrirEditor}>Crear Wiki</button>
            </form>
        </>
      ) : (
        <EditorWiki wiki={null}
        onCancelar={handleCerrarEditor}
        onWikiUpdated={null}/>
      )}
    </>
  );
}

export default PantallaInicio;
