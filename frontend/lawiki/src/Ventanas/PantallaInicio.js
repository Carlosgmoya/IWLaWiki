import React from "react";
import { useEffect, useState } from "react";
import './PantallaInicio.css';
function PantallaInicio() {

    const [listaWikis, setlistaWikis] = useState("");

    // Peticion fetch
    useEffect(() => {
        fetch("http://127.0.0.1:8001/api/v1/wikis")
          .then((response) => response.json())
          .then((data) => {
            if (Array.isArray(data)) {
              setlistaWikis(data); // Almacena la lista completa de wikis
            } else {
              console.error("Error: La respuesta no es una lista.");
            }
          })
          .catch((error) => console.error("Error al obtener la lista de wikis:", error));
      }, []);
    

    return (<>
        <div className="Titulo">
          <h1>La Wiki:</h1>
        </div>

        <form>
          <input type="text"/>
        </form>

        <div>
          <h2>Articulos Recientes</h2>
          <div>
            Futura lista de articulos recientes
          </div>
        </div>

        <div>
          <h2>Wikis Destacadas</h2>
          {listaWikis.length > 0 ? (
            <ul>
                {listaWikis.map((listaWikis, index) => (
                    <li><a href={`http://localhost:3000/wikis/${listaWikis.nombre}`}>{listaWikis.nombre}</a></li>
                ))}
            </ul>
          ) : (
            <p>No hay wikis disponibles</p>
          )}
        </div>
        
       
    </>);
}
export default PantallaInicio;