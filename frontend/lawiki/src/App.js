import './App.css';
import { BrowserRouter as Router, Routes, Route } from "react-router-dom";
import PantallaInicio from './Ventanas/PantallaInicio';
import WikiDetalle from './Ventanas/WikiDetalle';
import ArticuloDetalle from './Ventanas/ArticuloDetalle';

function App() {
  return (
    <>
      <div> {/*ESTO ES EL HEADER*/}
        <h1><a href='http://localhost:3000/'>LaWiki</a></h1> 
        
      </div>
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
    </>

    
  );
}

export default App;
