import React, { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";

import EditorWiki from "../Componentes/EditorWiki";
import CrearArticulo from "../Componentes/CrearArticulo";
import ListaArticulo from "../Componentes/ListaArticulo";
import { useSesion } from "../Login/authContext";
import { tienePermiso } from "../Login/auth";

import '../Estilos/VentanaWiki.css';

function VentanaWiki() {
  const backendURL = process.env.REACT_APP_BACKEND_URL;

  const { nombre } = useParams(); // Obtener el nombre de la URL
  const { rolUsuario } = useSesion();

  const [wiki, setWiki] = useState(null);
  const [mostrarEditor, setMostrarEditor] = useState(false);
  const [mostrarCrearArticulo, setMostrarArticulo] = useState(false);

  const fetchWikiDatos = useCallback(async () => {
    try {
      const response = await fetch(`${backendURL}/wikis/${nombre}`);
      const data = await response.json();
      setWiki(data);
    } catch (error) {
      console.error("Error al obtener los detalles de la wiki:", error);
    }
  }, [nombre]);


  const handleAbrirEditor = () => {
    setMostrarArticulo(false);
    setMostrarEditor(true); // Muestra el editor
  };

  const handleCerrarEditor = () => {
    setMostrarEditor(false);
  };

  const handleAbrirCrearArticulo = () => {
    setMostrarEditor(false);
    setMostrarArticulo(true);
  };

  const handleCerrarCrearArticulo = () => {
    setMostrarArticulo(false);
  };

  const handleWikiActualizada = (wikiActualizada) => {
    setWiki(wikiActualizada); // Actualiza la wiki localmente.
    fetchWikiDatos(); // Refresca los datos desde el servidor.
    setMostrarEditor(false);
  };

  useEffect(() => {
    fetchWikiDatos();
  }, []);

  return (
    <div>
      {wiki ? (
        <>
          <div className="cabeceraWiki">
            <h1 className="nombreWiki">{wiki.nombre}</h1>
            {
            (tienePermiso(rolUsuario, "editarWiki")) &&
            (!mostrarEditor && !mostrarCrearArticulo) && (
              <button title="Editar wiki" className="botonEditar" onClick={handleAbrirEditor}>
                <img src="/Iconos/IconoEditar.svg" alt="Editar wiki" />
              </button>
              )
            }
          </div>

          {!mostrarEditor && !mostrarCrearArticulo ? (
            <>
              <p>{wiki.descripcion}</p>
              <ListaArticulo nombreWiki={nombre}/>

              {
              tienePermiso(rolUsuario, "crearArticulo") &&
              <div>  
                <button className="irACrearArticulo" onClick={handleAbrirCrearArticulo}>Crear Artículo</button>
              </div>
              }
            </>
          ) : (
            <>
              {mostrarEditor ? (
                <EditorWiki wiki={wiki}
                  onCancelar={handleCerrarEditor}
                  onWikiActualizado={handleWikiActualizada} />
              ) : (
                <CrearArticulo nombreWiki={nombre}
                  onCancelar={handleCerrarCrearArticulo} />
              )}
            </>
          )}
        </>
      ) : (
        <p>Cargando detalles de la wiki...</p>
      )}
    </div>
  );
}

export default VentanaWiki;
