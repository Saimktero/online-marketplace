import { useEffect, useState } from 'react';
import { getProducts } from './api/products';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import Login from './pages/Login';
import Catalog from './pages/Catalog';
import NavBar from './components/NavBar';
import Cart from './components/Cart';
import MyOrders from './components/MyOrders'
import Products from './pages/Products'
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';
import axiosInstance from './axiosInstance';


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

  async function handleCheckout() {
    try {
      const orderData = {
        items: cartItems.map(item =>  ({
          product_id: item.id,
          quantity: item.quantity
        }))
      };

      const response = await axiosInstance.post('http://127.0.0.1:8000/api/orders/', orderData);

      if (response.status === 201) {
        toast.success('Заказ успешно создан');
        setCartItems([]);
        setReloadOrders(prev => !prev);
      } else {
        toast.success('Ошибка при оформлении заказа');
      }

    } catch (error) {
      console.error('Ошибка при оформлении заказа', error);
      toast.error('Ошибка при оформлении заказа');
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
      const response = await axiosInstance.get('http://localhost:8000/api/products/');
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
    axiosInstance.get(url).then(response => {
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
      <ToastContainer position='top-right' autoClose={3000} />
    </Router>
  );
}

export default App;

