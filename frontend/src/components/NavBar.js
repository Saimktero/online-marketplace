import { Link, useNavigate } from 'react-router-dom';

function NavBar() {
  const navigate = useNavigate();
  const isAuthenticated = !!localStorage.getItem('access');

  const handeLogout = () => {
    localStorage.removeItem('access');
    localStorage.removeItem('refresh');
    navigate('/login');
  };

  return (
    <nav>
      <Link to='/'>Главная</Link>
      <Link to='/catalog'>Каталог</Link>
      <Link to='/cart'>Корзина</Link>
      {isAuthenticated ? (
      <>
        <Link to='/my-orders'>Мои заказы</Link>
        <button onClick={handeLogout}>Выйти</button>
      </>
      ) : (
        <Link to='/login'>Войти</Link>
      )}
    </nav>
  );
}

export default NavBar;