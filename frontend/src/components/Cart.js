import React from 'react';

function Cart({ cartItems, handleCheckout }) {
  return (
    <div>
      <h2>Корзина</h2>
      {cartItems.length === 0 ? (
        <p>Ваша корзина пуста.</p>
      ) : (
        cartItems.map(item => (
          <div key={item.id}>
            <p>{item.name} - Количество: {item.quantity}</p>
          </div>
        ))
      )}

      {cartItems.length > 0 && (
        <button onClick={handleCheckout}>Оформить заказ</button>
      )}
    </div>
  );
}

export default Cart;