import React,  { createContext, useState } from 'react';
import Product from './Product';

function ProductList({ products, addToCart }) {
  return (
    <div>
      <ul>
        {products.length > 0 ? (
          products.map(product => (
            <Product
             key={product.id}
             name={product.name}
             addToCart={() => addToCart(product)}
             />
          ))
         ) : (
           <p>Загрузка товаров...</p>
         )}
       </ul>
    </div>
  );
}

export default ProductList;