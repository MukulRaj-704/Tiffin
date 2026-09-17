import api from './api';

export const login = async (username, password) => {
  const response = await api.post('/auth/login/', { username, password });
  const { access, refresh } = response.data;
  localStorage.setItem('accessToken', access);
  localStorage.setItem('refreshToken', refresh);
  return response.data;
};

export const getCurrentUser = async () => {
  const response = await api.get('/auth/me/');
  return response.data;
};
