import '../Estilos/Cabecera.css';
import { Link } from 'react-router-dom';

function Cabecera() {
    return <header>
                <h1><Link class="lawiki" to='/' reloadDocument>laWiki</Link></h1>
            </header>;
}

export default Cabecera;