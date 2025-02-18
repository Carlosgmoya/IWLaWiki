import React, { useEffect, useState } from "react";
import { Link, useParams } from "react-router-dom";

import Comentarios from '../Componentes/Comentarios';
import VerArticulo from "../Componentes/VerArticulo";
import VerMapa from "../Componentes/VerMapa";
import EditorArticulo from "../Componentes/EditorArticulo";
import { useSesion } from "../Login/authContext";
import { tienePermiso } from "../Login/auth";

import "../Estilos/VentanaArticulo.css";

function VentanaArticulo() {
    const backendURL = process.env.REACT_APP_BACKEND_URL;

    const { nombreUsuario, rolUsuario } = useSesion();

    const { nombre } = useParams();
    const { titulo } = useParams();
    const [articulo, setArticulo] = useState(null);   //JSON: 
    const [creador, setCreador] = useState(null);     //JSON: nombre, email
    const [mostrarComentarios, setMostrarComentarios] = useState(false);
    const [mostrarEditor, setMostrarEditor] = useState(false);
    const [articuloMio, setArticuloMio] = useState(false);

    useEffect(() => {
        const fetchData = async () => {
            try {
                const respuesta1 = await fetch(`${backendURL}/wikis/${nombre}/articulos/${titulo}`);
                const datosArticulo = await respuesta1.json();
                setArticulo(datosArticulo); // Almacena la lista completa de articulos

                const respuesta2 = await fetch(`${backendURL}/usuarios/id/${datosArticulo.creador.$oid}`);
                const datosCreador = await respuesta2.json();
                setCreador(datosCreador);

                if (nombreUsuario === datosCreador.nombre) {
                    setArticuloMio(true);
                } else {
                    setArticuloMio(false);
                }
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

    return (
    <div className="paginaArticulo">
        <div className="cabeceraWiki">
            <h1 className="nombreWiki"><Link to={`/wikis/${nombre || 'defaultNombre'}`}>{nombre}</Link></h1>
        </div>
        {(articulo && creador) ? (
            <>
                <div className="articulo">
                    <div className="cabeceraArticulo">
                        <h1 className="tituloArticulo">{articulo.titulo}</h1>
                        {
                        !mostrarEditor &&
                        (
                            <div>
                                {tienePermiso(rolUsuario, "editarArticuloMio") &&
                                articuloMio &&
                                <button title="Versiones anteriores del artículo" className="botonHistorial">
                                    <Link to={`/wikis/${nombre}/${titulo}/historial`}>
                                        <img src="/Iconos/IconoHistorial.svg" alt="Versiones anteriores del artículo" />
                                    </Link>
                                </button>
                                }
                                <button title="Creador del artículo" className="botonCreador">
                                    <Link to={`/usuario/${creador.nombre || 'defaultCreador'}`}>
                                        <img src="/Iconos/IconoPerfil.svg" alt="Creador del artículo" />
                                    </Link>
                                </button>
                                
                                {tienePermiso(rolUsuario, "editarArticulo") &&
                                <button title="Editar artículo" className="botonEditar" onClick={handleAbrirEditor}>
                                    <img src="/Iconos/IconoEditar.svg" alt="Editar articulo" />
                                </button>
                                }
                            </div>
                        )
                        }

                    </div>
                    {!mostrarEditor ? (
                        <>
                            <div className="cuerpoArticulo">
                                <div className="contenidoArticulo">
                                    <VerArticulo contenido_html={articulo.contenido_html} />
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
                            <div className="contenedorComentarios">
                                <button className="botonComentarios" onClick={() => setMostrarComentarios(!mostrarComentarios)}>
                                    <img src="/Iconos/Comentarios.svg" alt="Comentarios" />
                                    <p>Comentarios</p>
                                </button>
                            </div>
                            {mostrarComentarios ?
                                <Comentarios
                                    emailCreador={creador.email}
                                /> : null
                            }
                        </>
                    ) : (
                        <EditorArticulo
                            nombreWiki={nombre}
                            tituloArticulo={titulo}
                            contenidoInicial={articulo.contenido}
                            emailCreador={creador.email}
                            idioma={articulo.idioma}
                            creadorId={creador._id}
                            onCancelar={handleCerrarEditor}
                        />
                    )}
                </div>
            </>
        ) : (
            <p>Cargando...</p>
        )}
    </div>);
}
export default VentanaArticulo;