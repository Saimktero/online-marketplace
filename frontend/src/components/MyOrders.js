import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const MyOrders = () => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchOrders = async () => {
      try {
        const token = localStorage.getItem('access');
        if (!token) {
          navigate('/login');
          return;
        }

        const response = await axios.get('/api/orders/', {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        });

        console.log('Ответ сервера:', response.data);
        setOrders(response.data.results);
      } catch (err) {
        setError('Не удалось загрузить заказы.');
      } finally {
        setLoading(false);
      }
    };

    fetchOrders();
  }, [navigate]);

  if (loading) return <p>Загрузка заказов..</p>;
  if (error) return <p style={{ color: 'red' }}>{error}</p>;

  return (
    <div>
      <h2>Мои заказы</h2>
      {!Array.isArray(orders) || orders.length === 0 ? (
        <p>У вас нет заказов.</p>
      ) : (
        <ul>
          {orders.map(order => (
            <li key={order.id}>
              <strong>№{order.id}</strong> — {order.total_price}₽ — {new Date(order.created_at).toLocaleDateString()}
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default MyOrders