import axiosInstance from '../axiosInstance';

export const getProducts = async (page = 1) => {
  const response = await axiosInstance.get(`http://localhost:8000/api/products/?page=${page}`);
  return response.data;
};