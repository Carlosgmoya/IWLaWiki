import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function WikiDetalle() {
  const { nombre } = useParams(); // Obtener el nombre de la URL
  const [wiki, setWiki] = useState(null); // Estado para almacenar los detalles de la wiki
  const [listaArticulos, setlistaArticulos] = useState([]);

  useEffect(() => {
    // Petición al backend para obtener la wiki por nombre
    fetch(`http://127.0.0.1:8001/api/v1/wikis/${nombre}`)
      .then((response) => response.json())
      .then((data) => setWiki(data))
      .catch((error) => console.error("Error al obtener los detalles de la wiki:", error));


    fetch(`http://127.0.0.1:8002/api/v1/wikis/${nombre}/articulos`)
    .then((response) => response.json())
          .then((data) => {
            if (Array.isArray(data)) {
              setlistaArticulos(data); // Almacena la lista completa de articulos
            } else {
              console.error("Error: La respuesta no es una lista.");
            }
          })
          .catch((error) => console.error("Error al obtener la lista de articulos:", error));

  }, [nombre]);

  return (
    <div>
      {wiki ? (
        <>
          <h1>{wiki.nombre}</h1>
          <p>{wiki.descripcion}</p>
          {listaArticulos.length > 0 ? (
            <ul>
                {listaArticulos.map((listaArticulos, index) => (
                <li key={index}>{listaArticulos.titulo}</li> // Asumiendo que cada wiki tiene un campo `nombre`
                ))}
            </ul>
        ) : (
        <p>No hay articulos disponibles</p>
      )}
          
        </>
      ) : (
        <p>Cargando detalles de la wiki...</p>
      )}
    </div>
  );
}

export default WikiDetalle;