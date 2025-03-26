import { useState } from 'react';
import axiosInstance from '../axiosInstance';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify'


function LoginForm({ loadProducts }) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleLogin = async (event) => {
    event.preventDefault();
    setError(null);

    try {
      const response = await axiosInstance.post('http://localhost:8000/api/users/token/', {
        username,
        password,
      });

      localStorage.setItem('access', response.data.access);
      localStorage.setItem('refresh', response.data.refresh);

      toast.success('Успешный вход в аккаунт');
      loadProducts();
      navigate('/products');
    } catch (err) {
      toast.error('Ошибка авторизации: неверные данные')
      setError('Ошибка авторизации');
    }
  };

  return (
    <div>
      <h2>Вход</h2>
      <form onSubmit={handleLogin}>
        <input
          type='text'
          placeholder='Логин'
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          required
        />
        <input
          type='password'
          placeholder='Пароль'
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          required
        />
        <button type='sumbit'>Войти</button>
      </form>
      {error ? <p>{error}</p> : null}
    </div>
  );
}

export default LoginForm