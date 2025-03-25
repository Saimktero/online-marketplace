import ProductList from '../components/ProductList';
import Pagination from '../components/Pagination';

function Products({ products, nextPage, prevPage, loadPage, addToCart }) {
  return (
    <div>
      <h2>Каталог товаров</h2>
      <ProductList products={products} addToCart={addToCart} />
      <Pagination nextPage={nextPage} prevPage={prevPage} loadPage={loadPage} />
      </div>
  );
}

export default Products;