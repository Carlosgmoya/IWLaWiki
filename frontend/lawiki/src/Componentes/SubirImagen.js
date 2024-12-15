import React, { useState } from "react";

const SubirImagen = () => {
    const [message, setMessage] = useState('');
    const [file, setFile] = useState(null);

    const handleFileChange = (e) => {
        setFile(e.target.files[0]); 
    };

    const handleSubirImagen = async (e) => {
        e.preventDefault();
        if (!file) {
            setMessage("Por favor, selecciona un archivo.");
            return;
        }
        const formData = new FormData();
        formData.append("archivo", file); // El nombre "archivo" es el nombre del campo que usaremos en el backend
        try {
            const response = await fetch(
                `http://localhost:8000/subirImagen`,
                {
                    method: "POST",
                    body: formData,
                }
            );
            if (response.ok) {
                const respuestaTexto = await response.text(); // Leer la respuesta como texto
                setMessage(respuestaTexto); // Asignar el mensaje o enlace al estado
            } else {
                const errorData = await response.json();
                console.error("Error:", errorData);
                setMessage("Error al guardar el artículo.");
            }
        } catch (error) {
            console.error("Error:", error);
            setMessage("Error inesperado al conectar con el servidor.");
        }
    };

    return (
        <div>
            <form onSubmit={handleSubirImagen}>
                <label>
                    Selecciona una imagen:
                    <input
                        type="file"
                        onChange={handleFileChange}
                    />
                </label>
                <button type="submit">Subir Imagen</button>
            </form>
            {message && <p>{message}</p>} {/* Muestra el mensaje de respuesta */}
        </div>
    );
};

export default SubirImagen;
