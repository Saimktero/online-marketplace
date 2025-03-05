import axios from 'axios';

export const getProducts = async (page = 1) => {
  const response = await axios.get(`http://localhost:8000/api/products/?page=${page}`);
  return response.data;
};