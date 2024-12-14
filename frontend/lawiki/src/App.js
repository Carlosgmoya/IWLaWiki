import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";

import HeaderWiki from './Componentes/HeaderWiki';
import PantallaInicio from './Ventanas/PantallaInicio';
import WikiDetalle from './Ventanas/WikiDetalle';
import ArticuloDetalle from './Ventanas/ArticuloDetalle';
import UsuarioDetalle from './Ventanas/UsuarioDetalle';

function App() {
  return (
    <>
      <div class="cabecera">
        <HeaderWiki />
      </div>

      <div className="pagina">
        <Router>
          <Routes>
            <Route
              path="/"
              element={<PantallaInicio />}
            />

            <Route 
              path="/wikis/:nombre" 
              element={<WikiDetalle />} /> {/* Ruta dinámica */}

            <Route 
            path="/wikis/:nombre/:titulo"
            element={<ArticuloDetalle/>}
            />

            <Route
              path="/usuario/:nombre"
              element={<UsuarioDetalle/>}
            />  
          </Routes>
        </Router>
      </div>
    </>

    
  );
}

export default App;
