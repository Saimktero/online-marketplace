import React, { useEffect, useState } from 'react';
import axiosInstance from '../axiosInstance';
import { useNavigate } from 'react-router-dom';
import { toast } from 'react-toastify';

const MyOrders = ({ reloadTrigger }) => {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchAllOrders = async () => {
      try {
        const token = localStorage.getItem('access');
        if (!token) {
          navigate('/login');
          return;
        }

        let url = '/api/orders/';
        let allOrders = [];

        while (url) {
          const response = await axiosInstance.get(url)
          allOrders = [...allOrders, ...response.data.results];
          url = response.data.next;
        }

        setOrders(allOrders);
      } catch (err) {
        toast.error('Не удалось загрузить заказы.');
        setError('Не удалось загрузить заказы.');
      } finally {
        setLoading(false);
      }
    };

    fetchAllOrders();
  }, [navigate, reloadTrigger]);

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