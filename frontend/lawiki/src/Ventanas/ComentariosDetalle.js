import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import ComentariosArticulo from '../Componentes/ComentariosArticulo';

function ComentariosDetalle() {
    const { nombre } = useParams();
    const { titulo } = useParams();
    const [listaComentarios, setListaComentarios] = useState([]);

    useEffect(() => {
        fetch(`http://localhost:8000/wikis/${nombre}/articulo/${titulo}/comentarios`)
        .then((response) => response.json())
        .then((data) => {
            console.log(data)
            setListaComentarios(data);
        })
    }, [nombre, titulo])

    return (<>
        <ComentariosArticulo listaComentarios={listaComentarios}/>

        <p><Link to={`/wikis/${nombre || 'defaultNombre'}/${titulo || 'defaultTitulo'}`}>Volver al artículo</Link></p>
    </>);
}
export default ComentariosDetalle;