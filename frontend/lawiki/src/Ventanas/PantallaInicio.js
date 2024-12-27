import React, {  useState } from "react";

import EditorWiki from "../Componentes/EditorWiki";
import ListaWiki from "../Componentes/ListaWiki";
import { useSesion } from "../Login/authContext";
import { tienePermiso } from "../Login/auth";

import '../Estilos/PantallaInicio.css';

function PantallaInicio() {
  const { rolUsuario } = useSesion();

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
            
            {tienePermiso(rolUsuario, "crearWiki") &&
            <form>
              <button className="botonIrACrearWiki" onClick={handleAbrirEditor}>Crear Wiki</button>
            </form>
            }
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
