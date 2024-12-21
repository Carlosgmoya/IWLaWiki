import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import { ToastContainer } from "react-toastify";
import "react-toastify/dist/ReactToastify.css";

import { Sesion } from './Login/authContext';
import Cabecera from './Componentes/Cabecera';
import PantallaInicio from './Ventanas/PantallaInicio';
import VentanaWiki from './Ventanas/VentanaWiki';
import VentanaArticulo from './Ventanas/VentanaArticulo';
import VentanaUsuario from './Ventanas/VentanaUsuario';

function App() {
  return (
    <Sesion>
      <Router>

        <div class="cabecera">
          <Cabecera />
        </div>

        <div className="pagina">
          <Routes>
            <Route
              path="/"
              element={<PantallaInicio />}
            />

            <Route
              path="/wikis/:nombre"
              element={<VentanaWiki />} 
            /> {/* Ruta dinámica */}

            <Route
              path="/wikis/:nombre/:titulo"
              element={<VentanaArticulo />}
            />

            <Route
              path="/usuario/:nombre"
              element={<VentanaUsuario />}
            />
          </Routes>
        </div>
      </Router>
      <ToastContainer />
    </Sesion>


  );
}

export default App;
