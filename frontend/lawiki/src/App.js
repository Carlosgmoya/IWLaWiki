import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PantallaInicio from './Ventanas/PantallaInicio';
import WikiDetalle from './Ventanas/WikiDetalle';
import ArticuloDetalle from './Ventanas/ArticuloDetalle';
import HeaderWiki from './Componentes/HeaderWiki';

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
          </Routes>
        </Router>
      </div>
    </>

    
  );
}

export default App;
