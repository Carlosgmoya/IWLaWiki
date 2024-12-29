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
    <div className="pantallaInicio">
      {!mostrarCrearWiki ? (
        <>
        <ListaWiki/ >
            
            {tienePermiso(rolUsuario, "crearWiki") &&
            <div className="contenedorBotonCrear">
              <button className="botonIrACrearWiki" onClick={handleAbrirEditor}>Crear Wiki</button>
            </div>
            }
        </>
      ) : (
        <EditorWiki wiki={null}
        onCancelar={handleCerrarEditor}
        onWikiUpdated={null}/>
      )}
    </div>
  );
}

export default PantallaInicio;
