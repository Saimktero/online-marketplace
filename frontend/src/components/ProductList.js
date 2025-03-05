import Product from './Product';

function ProductList({ products }) {
  return (
    <div>
      <ul>
        {products.length > 0 ? (
          products.map(product => (
            <Product key={product.id} name={product.name} />
          ))
         ) : (
           <p>Загрузка товаров...</p>
         )}
       </ul>
    </div>
  );
}

export default ProductList;