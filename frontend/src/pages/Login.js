import LoginForm from '../components/LoginForm';

function Login({ loadProducts }) {
  return(
    <div>
    <h1>Страница входа</h1>
    <LoginForm loadProducts={loadProducts} />
    </div>
  );
}

export default Login;