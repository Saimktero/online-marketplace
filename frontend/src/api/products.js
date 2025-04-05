import axiosInstance from '../axiosInstance';

const API = process.env.REACT_APP_API_BASE_URL;

export const getProducts = async (page = 1) => {
  const response = await axiosInstance.get(`${API}/products/?page=${page}`);
  return response.data;
};