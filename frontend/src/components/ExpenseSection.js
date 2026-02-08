import { useState } from 'react';
import * as api from '../api';

function ExpenseSection({ users, onExpenseAdded }) {
  const [description, setDescription] = useState('');
  const [amount, setAmount] = useState('');
  const [paidBy, setPaidBy] = useState('');
  const [splitBetween, setSplitBetween] = useState([]);
  const [date, setDate] = useState(new Date().toISOString().split('T')[0]);
  const [error, setError] = useState('');
  const [splitError, setSplitError] = useState('');
  const [success, setSuccess] = useState('');

  const handleAddExpense = async (e) => {
    e.preventDefault();
    setError('');
    setSplitError('');
    setSuccess('');

    // Validation
    if (!description.trim()) {
      setError('Please enter a description');
      return;
    }

    if (!amount || parseFloat(amount) <= 0) {
      setError('Please enter a valid amount');
      return;
    }

    if (!paidBy) {
      setError('Please select who paid');
      return;
    }

    if (splitBetween.length === 0) {
      setSplitError('Please select at least one user');
      return;
    }

    try {
      await api.addExpense({
        description,
        amount: parseFloat(amount),
        paid_by: paidBy,
        split_between: splitBetween,
        date,
      });

      // Reset form
      setDescription('');
      setAmount('');
      setPaidBy('');
      setSplitBetween([]);
      setDate(new Date().toISOString().split('T')[0]);

      setSuccess('Expense added successfully!');
      setTimeout(() => setSuccess(''), 3000);

      onExpenseAdded({ users: false, expenses: true, settlement: true });
    } catch (err) {
      setError(err.response?.data?.detail || 'Error adding expense');
    }
  };

  const handleSplitCheck = (userName) => {
    setSplitBetween((prev) =>
      prev.includes(userName)
        ? prev.filter((p) => p !== userName)
        : [...prev, userName]
    );
  };

  return (
    <div className="card">
      <h2>💵 Add Expense</h2>

      <form onSubmit={handleAddExpense}>
        <div className="form-group">
          <label htmlFor="description">Description</label>
          <input
            type="text"
            id="description"
            placeholder="e.g., Dinner at Mario's"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            autoComplete="off"
          />
        </div>

        <div className="form-group">
          <label htmlFor="amount">Amount (Rs)</label>
          <input
            type="number"
            id="amount"
            placeholder="e.g., 1200"
            value={amount}
            onChange={(e) => setAmount(e.target.value)}
            min="0"
            step="0.01"
          />
        </div>

        <div className="form-group">
          <label htmlFor="paidBy">Who Paid?</label>
          <select
            id="paidBy"
            value={paidBy}
            onChange={(e) => setPaidBy(e.target.value)}
          >
            <option value="">-- Select User --</option>
            {users.map((user) => (
              <option key={user} value={user}>
                {user}
              </option>
            ))}
          </select>
        </div>

        <div className="form-group">
          <label>Split Between (select multiple)</label>
          <div className="checkbox-group">
            {users.length === 0 ? (
              <div className="empty-state">No users added yet</div>
            ) : (
              users.map((user) => (
                <div key={user} className="checkbox-item">
                  <input
                    type="checkbox"
                    id={`split_${user}`}
                    checked={splitBetween.includes(user)}
                    onChange={() => handleSplitCheck(user)}
                  />
                  <label htmlFor={`split_${user}`}>{user}</label>
                </div>
              ))
            )}
          </div>
          {splitError && <div className="error">{splitError}</div>}
        </div>

        <div className="form-group">
          <label htmlFor="date">Date</label>
          <input
            type="date"
            id="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
          />
        </div>

        <button type="submit">Add Expense</button>
        {error && <div className="error">{error}</div>}
        {success && <div className="success">{success}</div>}
      </form>
    </div>
  );
}

export default ExpenseSection;
