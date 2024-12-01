import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import VerArticulo from "../Componentes/VerArticulo";
import EditarArticulo from "../Componentes/EditarArticulo";

function ArticuloDetalle() {
    const { nombre } = useParams();
    const { titulo } = useParams();
    const [articulo, setArticulo] = useState(null);
    const [mostrarEditor, setMostrarEditor] = useState(false);

    useEffect(() => {
        fetch(`http://127.0.0.1:8000/wikis/${nombre}/articulos/${titulo}`)
            .then((response) => response.json())
            .then((data) => {
                console.log("Datos del artículo:", data);
                setArticulo(data); // Almacena la lista completa de articulos         
            })
            .catch((error) => console.error("Error al obtener el articulos:", error));

    }, [nombre, titulo]);

    const handleAbrirEditor = () => {
        setMostrarEditor(true); // Muestra el editor
    };

    const handleCerrarEditor = () => {
        setMostrarEditor(false);
    };

    return (<>
        <h1><a href={`http://localhost:3000/wikis/${nombre}`}>{nombre}</a></h1>
        {articulo ? (
            <>
                <h1>{articulo.titulo}</h1>
                {!mostrarEditor ? (
                    <>
                        <VerArticulo contenido_html={articulo.contenido_html} />
                        <div>
                            <button onClick={handleAbrirEditor}>Editar Articulo</button>
                        </div>
                    </>
                ) : (
                    <>
                        <EditarArticulo
                            nombreWiki={nombre}
                            tituloArticulo={titulo}
                            contenidoInicial={articulo.contenido}
                        />
                        <div>
                            <button onClick={handleCerrarEditor}>Cancelar</button>
                        </div>
                    </>
                )}



            </>
        ) : (
            <p>Cargando...</p>
        )}
    </>);
}
export default ArticuloDetalle;