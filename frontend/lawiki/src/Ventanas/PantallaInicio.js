import React, { useEffect, useState } from "react";
import './PantallaInicio.css';
import ResultadosBusqueda from '../Componentes/ResultadosBusqueda';
import InicioDestacados from '../Componentes/InicioDestacados';
import EditorWiki from "../Componentes/EditorWiki";

function PantallaInicio() {
  const [listaWikis, setListaWikis] = useState([]);
  const [listaBusqueda, setListaBusqueda] = useState([]);
  const [searchTerm, setSearchTerm] = useState("");
  const [debouncedSearchTerm, setDebouncedSearchTerm] = useState(""); // Término con debounce.
  const [mostrarEditor, setMostrarEditor] = useState(false);

  // Petición fetch inicial
  useEffect(() => {
    fetchWikisDestacadas();
  }, []);

  useEffect(() => {
    // Configura un debounce: espera 300ms antes de actualizar el término de búsqueda.
    const handler = setTimeout(() => {
      setDebouncedSearchTerm(searchTerm);
    }, 300);

    return () => {
      clearTimeout(handler); // Limpia el temporizador si el usuario sigue escribiendo.
    };
  }, [searchTerm]);

  useEffect(() => {
    if (debouncedSearchTerm.trim()) {
      fetchBusqueda(debouncedSearchTerm);
    } else {
      setListaBusqueda([]); // Limpia los resultados si no hay término de búsqueda.
    }
  }, [debouncedSearchTerm]);

  const fetchWikisDestacadas = async () => {
    try {
      const response = await fetch("http://127.0.0.1:8000/wikis");
      const data = await response.json();
      if (Array.isArray(data)) {
        setListaWikis(data); // Carga las wikis destacadas.
      } else {
        console.error("Error: La respuesta no es una lista.");
      }
    } catch (error) {
      console.error("Error al obtener las wikis destacadas:", error);
    }
  };

  const fetchBusqueda = async (term) => {
    try {
      const response = await fetch(`http://127.0.0.1:8000/wikis?term=${term}`);
      const data = await response.json();
      if (Array.isArray(data)) {
        setListaBusqueda(data); // Actualiza los resultados de búsqueda.
      } else {
        console.error("Error: La respuesta no es una lista.");
      }
    } catch (error) {
      console.error("Error al buscar wikis:", error);
    }
  };

  const handleAbrirEditor = () => {
    setMostrarEditor(true); // Muestra el editor
  };

  const handleCerrarEditor = () => {
    // Restablece el formulario
    setMostrarEditor(false);
  };

  return (
    <>

      <div className="Titulo">
        <h1>La Wiki:</h1>
      </div>

      {!mostrarEditor ? (
        <>
          <div className="input">
            <input
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Buscar wikis..."
            />
          </div>

          {searchTerm !== "" ? (
            <ResultadosBusqueda listaBusqueda={listaBusqueda} nombrewiki={null} />
          ) : (
            <InicioDestacados listaWikis={listaWikis} />
          )}

          <form>
            <button onClick={handleAbrirEditor}>Crear Wiki</button>
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
