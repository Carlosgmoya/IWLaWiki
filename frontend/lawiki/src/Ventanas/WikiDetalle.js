import React, { useEffect, useState, useCallback } from "react";
import { useParams } from "react-router-dom";
import ArticulosWiki from "../Componentes/ArticulosWiki";
import ResultadosBusqueda from '../Componentes/ResultadosBusqueda';
import EditorWiki from "../Componentes/EditorWiki";

function WikiDetalle() {
  const { nombre } = useParams(); // Obtener el nombre de la URL
  const [wiki, setWiki] = useState(null);
  const [listaArticulos, setListaArticulos] = useState([]);
  const [listaBusqueda, setListaBusqueda] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState("");
  const [mostrarEditor, setMostrarEditor] = useState(false);

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
    setMostrarEditor(true); // Muestra el editor
  };

  const handleCerrarEditor = () => {
    // Restablece el formulario
    setMostrarEditor(false);
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
          <h1>{wiki.nombre}</h1>

          {!mostrarEditor ? (
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

              <form>
                <button onClick={handleAbrirEditor}>Modificar Wiki</button>
              </form>
            </>

          ) : (
            <EditorWiki  wiki={wiki}
            onCancelar={handleCerrarEditor}
            onWikiUpdated={handleWikiUpdated}/>

          )}



        </>




      ) : (
        <p>Cargando detalles de la wiki...</p>
      )}
    </div>
  );
}

export default WikiDetalle;
