import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import ComentariosArticulo from '../Componentes/ComentariosArticulo';
import VerArticulo from "../Componentes/VerArticulo";
import VerMapa from "../Componentes/VerMapa";
import EditarArticulo from "../Componentes/EditarArticulo";
import SubirImagen from "../Componentes/SubirImagen";
import SubirMapa from "../Componentes/SubirMapa";
import "../Estilos/Articulo.css";

function ArticuloDetalle() {
  const { nombre } = useParams();
  const { titulo } = useParams();
  const [articulo, setArticulo] = useState(null);   //JSON: 
  const [creador, setCreador] = useState(null);     //JSON: nombre, email
  const [mostrarComentarios, setMostrarComentarios] = useState(false);
  const [mostrarEditor, setMostrarEditor] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const response1 = await fetch(`http://lawiki-gateway:8000/wikis/${nombre}/articulos/${titulo}`);
                const datosArticulo = await response1.json();
                setArticulo(datosArticulo); // Almacena la lista completa de articulos

                const response2 = await fetch(`http://lawiki-gateway:8000/usuarios/id/${datosArticulo.creador.$oid}`);
                const datosCreador = await response2.json();
                setCreador(datosCreador);
                } catch (error) {
                    console.error("Error al obtener datos:", error);
                }
        };
        fetchData();
    }, [nombre, titulo]);


    const handleAbrirEditor = () => {
        setMostrarEditor(true); // Muestra el editor
    };

    const handleCerrarEditor = () => {
        setMostrarEditor(false);
    };

    return (<>
        <div className="cabeceraWiki">
            <h1 className="nombreWiki"><Link to={`http://localhost:3000/wikis/${nombre}`}>{nombre}</Link></h1>
        </div>
        {(articulo && creador) ? (
            <>
            <div className="articulo">
                <div className="cabeceraArticulo">
                    <h1 className="tituloArticulo">{articulo.titulo}</h1>
                    {!mostrarEditor &&
                        (
                        <div>
                            <Link to={`/usuario/${creador.nombre}`}>Creador</Link>
                            <button title="Editar artículo" className="botonEditar" onClick={handleAbrirEditor}>
                                <img src="/Iconos/IconoEditar.svg" alt="Editar articulo" />
                            </button>
                        </div>
                        )
                    }
                    
                </div>
                {!mostrarEditor ? (
                    <div className="cuerpoArticulo">
                        <div className="contenidoArticulo">
                            <VerArticulo contenido_html={articulo.contenido_html} />
                            <button className="botonComentarios" onClick={() => setMostrarComentarios(!mostrarComentarios)}>
                                <img src="/Iconos/Comentarios.svg" alt="Comentarios" />
                                <p>Comentarios</p>
                            </button>
                            {mostrarComentarios ?
                            <ComentariosArticulo/> : null
                            }
                        </div>
                        <div className="informacionArticulo">
                            <h3>Ubicación</h3>
                            <div className="contenedorMapa">
                            <VerMapa
                                nombreWiki={nombre}
                                tituloArticulo={titulo}
                            />
                            </div>
                        </div>
                    </div>
                ) : (
                    <>
                        <EditarArticulo
                            nombreWiki={nombre}
                            tituloArticulo={titulo}
                            contenidoInicial={articulo.contenido}
                            onCancelar={handleCerrarEditor}
                        />
                        <div>
                            <button onClick={handleCerrarEditor}>Cancelar</button>
                        </div>
                        <div>
                            <h1>Subir Imagen</h1>
                            <SubirImagen />
                        </div>
                        <div>
                            <SubirMapa
                                nombreWiki={nombre}
                                tituloArticulo={titulo}
                            />
                        </div>
                    </>
                )}
                </div>
            </>
        ) : (
            <p>Cargando...</p>
        )}
    </>);
}
export default ArticuloDetalle;