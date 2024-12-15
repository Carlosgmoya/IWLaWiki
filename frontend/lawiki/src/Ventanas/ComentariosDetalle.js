import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";

import ComentariosArticulo from '../Componentes/ComentariosArticulo';

function ComentariosDetalle() {
    const { nombre } = useParams();
    const { titulo } = useParams();
    const [listaComentarios, setListaComentarios] = useState([]);

    useEffect(() => {
        fetch(`http://lawiki-gateway:8000/wikis/${nombre}/articulo/${titulo}/comentarios`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            setListaComentarios(data);
        })
    }, [nombre, titulo])

    return (<>
        <ComentariosArticulo listaComentarios={listaComentarios}/>

        <p><a href={`http://localhost:3000/wikis/${nombre}/${titulo}`}>Volver al artículo</a></p>
    </>);
}
export default ComentariosDetalle;