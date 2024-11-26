import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

function ArticuloDetalle() {
    const { nombre } = useParams();
    const { titulo } = useParams();
    const [ articulo, setArticulo ] = useState(null);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/wikis/${nombre}/articulos/${titulo}`)
        .then((response) => response.json())
        .then((data) => {   
            console.log("Datos del artículo:", data);       
            setArticulo(data); // Almacena la lista completa de articulos         
        })
        .catch((error) => console.error("Error al obtener el articulos:", error));

    }, [nombre,titulo]);
    
    return (<>
        <h1><a href={`http://localhost:3000/wikis/${nombre}`}>{nombre}</a></h1>
        {articulo ? (
            <>
                <h1>{articulo.titulo}</h1>
                <p>{articulo.contenido}</p>
            </>
        ) : (
            <p>Cargando...</p>
        )}
    </>);
}
export default ArticuloDetalle;