import axios from 'axios';

// Configure axios defaults
axios.defaults.baseURL = 'http://127.0.0.1:8000';

// Request interceptor to add auth token
axios.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('token');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
axios.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('token');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API endpoints
export const API_ENDPOINTS = {
  // Auth
  LOGIN: '/api/v1/auth/login',
  REGISTER: '/api/v1/auth/register',
  ME: '/api/v1/auth/me',
  
  // Products
  PRODUCTS: '/api/v1/products/',
  PRODUCT: (id: number) => `/api/v1/products/${id}`,
  
  // Cart
  CART: '/api/v1/cart/',
  CART_ADD: '/api/v1/cart/add',
  CART_ITEM: (id: number) => `/api/v1/cart/items/${id}`,
  
  // Orders
  ORDERS: '/api/v1/orders/',
  ORDER: (id: number) => `/api/v1/orders/${id}`,
  
  // Recommendations
  RECOMMENDATIONS: '/api/v1/recommendations/',
};

export default axios; 