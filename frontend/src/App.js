import { useState, useEffect, useCallback } from 'react';
import './App.css';
import * as api from './api';
import { REFRESH_PATTERNS } from './utils';
import UserSection from './components/UserSection';
import ExpenseSection from './components/ExpenseSection';
import ExpensesList from './components/ExpensesList';
import SettlementSummary from './components/SettlementSummary';

function App() {
  const [users, setUsers] = useState([]);
  const [expenses, setExpenses] = useState([]);
  const [settlement, setSettlement] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const fetchUsers = () => api.getUsers();
  const fetchExpenses = () => api.getExpenses();
  const fetchSettlement = () => api.getSettlement();
  
  // Memoize refresh since it makes multiple API calls and is passed to children
  const refresh = useCallback(async ({
    users = false,
    expenses = false,
    settlement = false,
  } = {}) => {
    try {
      setLoading(true);
      setError('');

      const tasks = [];

      if (users) tasks.push(fetchUsers().then(setUsers));
      if (expenses) tasks.push(fetchExpenses().then(setExpenses));
      if (settlement) tasks.push(fetchSettlement().then(setSettlement));

      await Promise.all(tasks);
    } catch (err) {
      setError(
        err.response?.data?.detail ||
        'Error fetching data. Make sure API is running on http://localhost:8000'
      );
    } finally {
      setLoading(false);
    }
  }, []);


  useEffect(() => {
    refresh(REFRESH_PATTERNS.ALL);
  }, [refresh]);

  return (
    <div className="app">
      <header className="header">
        <h1>💰 Expense Splitter</h1>
        <p>Track shared expenses with friends easily</p>
      </header>

      {error && (
        <div className="error-banner">
          <p>{error}</p>
        </div>
      )}

      {loading && (
        <div className="loading">Loading...</div>
      )}

      <div className="content">
        <div className="left-column">
          <UserSection users={users} onUpdate={refresh} />
          <ExpenseSection users={users} onExpenseAdded={refresh} />
        </div>

        <div className="right-column">
          <ExpensesList expenses={expenses} onDelete={refresh} />
          <SettlementSummary settlement={settlement} />
        </div>
      </div>
    </div>
  );
}

export default App;
