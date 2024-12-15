import '../Estilos/HeaderWiki.css';
import { Link } from 'react-router-dom';

function HeaderWiki() {
    return <header>
                <h1><Link class="lawiki" to='/'>laWiki</Link></h1>
            </header>;
}

export default HeaderWiki;