// src/auth.js
const roles = {
    admin: ["crearWiki", "editarWiki", "eliminarWiki", "crearArticulo", "editarArticulo", "eliminarArticulo"],
    redactor: ["crearArticulo", "editarArticulo", "editarArticuloMio"],
  };
  
  // Check if the user's role includes a specific permission
  export const tienePermiso = (rol, permiso) => {
    return roles[rol]?.includes(permiso);
  };
  