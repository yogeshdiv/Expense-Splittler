import axios from 'axios';

const API_BASE_URL = process.env.API_BASE_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
});

// Users endpoints
export const getUsers = async () => {
  const response = await api.get('/users');
  return response.data;
};

export const addUser = async (name) => {
  const response = await api.post('/users', { name });
  return response.data;
};

export const removeUser = async (name) => {
  const response = await api.delete(`/users/${name}`);
  return response.data;
};

// Expenses endpoints
export const getExpenses = async () => {
  const response = await api.get('/expenses');
  return response.data;
};

export const addExpense = async (expense) => {
  const response = await api.post('/expenses', expense);
  return response.data;
};

export const deleteExpense = async (expenseId) => {
  const response = await api.delete(`/expenses/${expenseId}`);
  return response.data;
};

// Settlement endpoints
export const getSettlement = async () => {
  const response = await api.get('/settlement');
  return response.data;
};

export default api;
