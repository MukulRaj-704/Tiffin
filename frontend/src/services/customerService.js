import api from './api';

export const fetchCustomers = async () => {
  const response = await api.get('/customers/');
  return response.data;
};

export const searchCustomers = async (phone) => {
  const response = await api.get('/customers/search/', { params: { phone } });
  return response.data;
};

export const createCustomer = async (customer) => {
  const response = await api.post('/customers/', customer);
  return response.data;
};
