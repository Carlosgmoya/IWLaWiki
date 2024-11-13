import React from "react";
import { useEffect, useState } from "react";

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
        <h1>Lista de Wikis:</h1>
        {listaWikis.length > 0 ? (
            <ul>
                {listaWikis.map((listaWikis, index) => (
                    <li><a href={`http://localhost:3000/wikis/${listaWikis.nombre}`}>{listaWikis.nombre}</a></li>
                ))}
            </ul>
        ) : (
        <p>No hay wikis disponibles</p>
      )}
    </>);
}
export default PantallaInicio;