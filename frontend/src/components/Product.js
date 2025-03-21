import Ract from 'react';

function Product({ name, addToCart }) {
  return (
    <li>
      <p>{name}</p>
      <button onClick={addToCart}>Добавиь в корзину</button>
    </li>
  );
}

export default Product;
