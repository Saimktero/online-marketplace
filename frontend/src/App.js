import { useEffect, useState } from 'react';
import { getProducts } from './api/products';

function App() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    getProducts().then(data => setProducts(data));
  }, []);

  return (
    <div>
      <header>
        <h1>Маркетплейс</h1>
      </header>
      <main>
        <h2>Каталог товаров</h2>
        <ul>
          {products.length > 0 ? (
            products.map(product => (
              <li key={product.id}>{product.name}</li>
            ))
          ) : (
            <p>Загрузка товаров...</p>
          )}
        </ul>
      </main>
      <footer>
        <p>&copy; 2025 Онлайн-маркетплейс</p>
      </footer>
    </div>
  );
}

export default App;

