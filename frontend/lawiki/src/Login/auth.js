// src/auth.js
const roles = {
    admin: ["crearWiki", "editarWiki", "eliminarWiki", "crearArticulo", "editarArticulo", "editarArticuloMio", "eliminarArticulo", "crearComentario", "crearValoracion"],
    redactor: ["crearArticulo", "editarArticulo", "editarArticuloMio", "crearComentario", "crearValoracion"],
  };
  
  // Check if the user's role includes a specific permission
  export const tienePermiso = (rol, permiso) => {
    return roles[rol]?.includes(permiso);
  };
  