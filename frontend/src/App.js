import { useEffect, useState } from 'react';
import { getProducts } from './api/products';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import Login from './pages/Login';
import Catalog from './pages/Catalog';
import NavBar from './components/NavBar';
import Cart from './components/Cart';
import MyOrders from './components/MyOrders'
import Products from './pages/Products'


function App() {
  const [products, setProducts] = useState([]);
  const [nextPage, setNextPage] = useState(null);
  const [prevPage, setPrevPage] = useState(null);
  const [reloadOrders, setReloadOrders] = useState(false);

  const [cartItems, setCartItems] = useState(() => {
    const savedCart = localStorage.getItem('cartItems');
    return savedCart ? JSON.parse(savedCart) : [];
  });

  useEffect(() => {
    localStorage.setItem('cartItems', JSON.stringify(cartItems));
  }, [cartItems]);

  async function refreshToken() {
    try {
      const refresh = localStorage.getItem('refresh');
      if (!refresh) {
        alert('Ошибка: Refresh-токен отсутствует. Авторизуйтесь заново.')
        return null;
      }

      const response = await axios.post('http://127.0.0.1:8000/api/token/refresh/', {
        refresh: refresh
      });

      const newAccessToken = response.data.access;
      localStorage.setItem('access', newAccessToken);
      return newAccessToken;

    } catch (error) {
      console.error('Ошибка при обновлении токена:', error);
      alert('Сессия истекла. Авторизуйтесь заново.')
      return null;
    }
  }

  async function handleCheckout() {
    try {
      let token = localStorage.getItem('access'); // Достаём токен
      console.log("Текущий токен:", token); // Проверяем, есть ли он

      if (!token) {
        alert('Ошибка: Токен отсутствует. Авторизуйтесь заново.')
        return;
      }

      const config = {
        headers: {
          Authorization: `Bearer ${token}`,
          'Content-type': 'application/json'
        }
      };

      const orderData = {
        items: cartItems.map(item =>  ({
          product_id: item.id,
          quantity: item.quantity
        }))
      };

      //  Логируем URL перед отправкой
      console.log("Отправка заказа на:", 'http://127.0.0.1:8000/api/orders/');
      console.log("Данные заказа:", orderData);

     // console.log('Отправка заказа...', orderData);

      const response = await axios.post('http://127.0.0.1:8000/api/orders/', orderData, config);

      if (response.status === 201) {
        alert('Заказ успешно создан');
        setCartItems([]);
        setReloadOrders(prev => !prev);
      } else {
        alert('Ошибка при оформлении заказа');
      }

    } catch (error) {
      console.error('Ошибка при оформлении заказа', error);

      if (error.response && error.response.status === 401) {
        console.log('Попытка обновить токен...');
        const newToken = await refreshToken();
        if (newToken) {
          handleCheckout(); // повторяем  запрос с новым токен
        } else {
          alert('Ошибка: Авторизуйтесь заново.');
        }
      } else {
        alert(`Ошибка при оформлении заказа: ${error.response?.data?.detail || 'Неизвестная ошибка'}`);
      }
    }
  }

    function addToCart(product) {
    const existingItem = cartItems.find(item => item.id === product.id);
    if (existingItem) {
      setCartItems(prevItems =>
        prevItems.map(item =>
          item.id === product.id
            ?  { ...item, quantity: item.quantity + 1}
            : item
        )
      );
    } else {
      setCartItems(prevItems => [ ...prevItems, { ...product, quantity: 1 }]);
    }
  }

  const loadProducts = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/products/');
      setProducts(response.data.results);
    } catch (error) {
      console.error('Ошибка загрузки товаров:', error);
    }
  };

  useEffect(() => {
    loadProducts();
    getProducts().then(data => {
      setProducts(data.results);
      setNextPage(data.next);
      setPrevPage(data.previous);
    });
  }, []);

  function loadPage(url) {
    axios.get(url).then(response => {
      setProducts(response.data.results);
      setNextPage(response.data.next);
      setPrevPage(response.data.previous);
    });
  }

  return (
    <Router>
      <NavBar />
      <div>
        <header>
          <h1>Маркетплейс</h1>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/catalog" element={<Catalog />} />
            <Route path="/login" element={<Login loadProducts={loadProducts} />} />
            <Route
              path="/products"
                element={
                  <Products
                    products={products}
                    nextPage={nextPage}
                    prevPage={prevPage}
                    loadPage={loadPage}
                    addToCart={addToCart}
                  />
                }
             />
            <Route path='/cart' element={<Cart cartItems={cartItems} handleCheckout={handleCheckout} />} />
            <Route path='/my-orders' element={<MyOrders reloadTrigger={reloadOrders} />} />
          </Routes>
        </main>
        <footer>
          <p>&copy; 2025 Онлайн-маркетплейс</p>
        </footer>
      </div>
    </Router>
  );
}

export default App;

