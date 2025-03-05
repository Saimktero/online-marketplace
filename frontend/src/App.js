import { useEffect, useState } from 'react';
import { getProducts } from './api/products';
import ProductList from './components/ProductList';
import axios from 'axios';
import Pagination from './components/Pagination';

function App() {
  const [products, setProducts] = useState([]);
  const [nextPage, setNextPage] = useState(null);
  const [prevPage, setPrevPage] = useState(null);

  useEffect(() => {
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
    <div>
      <header>
        <h1>Маркетплейс</h1>
      </header>
      <main>
        <h2>Каталог товаров</h2>
        <ProductList products={products} />
        <Pagination nextPage={nextPage} prevPage={prevPage} loadPage={loadPage} />
      </main>
      <footer>
        <p>&copy; 2025 Онлайн-маркетплейс</p>
      </footer>
    </div>
  );
}

export default App;

