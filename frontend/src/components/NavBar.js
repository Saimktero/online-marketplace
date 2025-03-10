import { Link } from 'react-router-dom';

function NavBar() {
  return (
    <nav>
      <Link to='/'>Главная</Link>
      <Link to='/catalog'>Каталог</Link>
      <Link to='/login'>Вход</Link>
    </nav>
  );
}

export default NavBar;