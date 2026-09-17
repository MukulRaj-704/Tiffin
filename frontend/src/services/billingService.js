import api from './api';

export const fetchBilling = async (customerId) => {
  const response = await api.get(`/billing/customer/${customerId}/`);
  return response.data;
};

export const generateBilling = async (month, customerId = null) => {
  const payload = { month };
  if (customerId) {
    payload.customer_id = customerId;
  }
  const response = await api.post('/billing/generate/', payload);
  return response.data;
};
