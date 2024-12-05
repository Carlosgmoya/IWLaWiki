import React, { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";
import ArticulosWiki from "../Componentes/ArticulosWiki";
import ResultadosBusqueda from '../Componentes/ResultadosBusqueda';
import EditorWiki from "../Componentes/EditorWiki";
import CrearArticulo from "../Componentes/CrearArticulo";
import '../Estilos/WikiDetalle.css';

function WikiDetalle() {
  const { nombre } = useParams(); // Obtener el nombre de la URL
  const [wiki, setWiki] = useState(null);
  const [listaArticulos, setListaArticulos] = useState([]);
  const [listaBusqueda, setListaBusqueda] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState("");
  const [mostrarEditor, setMostrarEditor] = useState(false);
  const [mostrarCrearArticulo, setMostrarArticulo] = useState(false);

  const fetchWikiDatos = useCallback(async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/wikis/${nombre}`);
      const data = await response.json();
      setWiki(data);
    } catch (error) {
      console.error("Error al obtener los detalles de la wiki:", error);
    }
  }, [nombre]);

  const fetchArticulosWiki = useCallback(async () => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/wikis/${nombre}/articulos`);
      const data = await response.json();
      if (Array.isArray(data)) {
        setListaArticulos(data);
      } else {
        console.error("Error: La respuesta no es una lista.");
      }
    } catch (error) {
      console.error("Error al obtener la lista de artículos:", error);
    }
  }, [nombre]);

  const fetchBusqueda = useCallback(async (term) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/wikis/${nombre}/articulos?terminoDeBusqueda=${term}`);
      const data = await response.json();
      if (Array.isArray(data)) {
        setListaBusqueda(data);
      } else {
        console.error("Error: La respuesta no es una lista.");
      }
    } catch (error) {
      console.error("Error al buscar artículos:", error);
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

  const handleWikiUpdated = (updatedWiki) => {
    setWiki(updatedWiki); // Actualiza la wiki localmente.
    fetchWikiDatos(); // Refresca los datos desde el servidor.
    setMostrarEditor(false);
  };

  useEffect(() => {
    fetchWikiDatos();
    fetchArticulosWiki();
  }, [fetchWikiDatos, fetchArticulosWiki]);

  useEffect(() => {
    const handler = setTimeout(() => {
      setDebouncedSearchTerm(searchTerm);
    }, 300);
    return () => clearTimeout(handler);
  }, [searchTerm]);

  useEffect(() => {
    if (debouncedSearchTerm.trim()) {
      fetchBusqueda(debouncedSearchTerm);
    } else {
      setListaBusqueda([]);
    }
  }, [debouncedSearchTerm, fetchBusqueda]);

  return (
    <div>
      {wiki ? (
        <>
          <div className="cabeceraWiki">
            <h1 className="tituloWiki">{wiki.nombre}</h1>
            <button title="Editar wiki" className="irAModificarWiki" onClick={handleAbrirEditor}>
              <img src="/Iconos/IconoEditar.svg" alt="Editar wiki" />
            </button>
          </div>

          {!mostrarEditor && !mostrarCrearArticulo ? (
            <>
              <p>{wiki.descripcion}</p>
              <div className="input">
                <input
                  type="text"
                  value={searchTerm}
                  onChange={(e) => setSearchTerm(e.target.value)}
                  placeholder="Buscar Artículos..."
                />
              </div>

              {searchTerm !== "" ? (
                <ResultadosBusqueda listaBusqueda={listaBusqueda} nombrewiki={nombre} />
              ) : (
                <ArticulosWiki listaArticulos={listaArticulos} nombre={nombre} />
              )}

              <div>  
                <button className="irACrearArticulo" onClick={handleAbrirCrearArticulo}>Crear Artículo</button>
              </div>
            </>

          ) : (
            <>
              {mostrarEditor ? (
                <EditorWiki wiki={wiki}
                  onCancelar={handleCerrarEditor}
                  onWikiUpdated={handleWikiUpdated} />
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

export default WikiDetalle;
