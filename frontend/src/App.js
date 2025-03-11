import { useEffect, useState } from 'react';
import { getProducts } from './api/products';
import axios from 'axios';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { Home } from './pages/Home';
import Login from './pages/Login';
import Products from './pages/Products';
import Catalog from './pages/Catalog';
import NavBar from './components/NavBar';


function App() {
  const [products, setProducts] = useState([]);
  const [nextPage, setNextPage] = useState(null);
  const [prevPage, setPrevPage] = useState(null);

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
            <Route path="/products" element={<Products products={products} nextPage={nextPage} prevPage={prevPage} loadPage={loadPage} />} />
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

