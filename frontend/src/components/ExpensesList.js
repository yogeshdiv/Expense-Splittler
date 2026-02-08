import * as api from '../api';
import { formatDate, REFRESH_PATTERNS } from '../utils';

function ExpensesList({ expenses, onDelete }) {
  const handleDelete = async (id) => {
    try {
      await api.deleteExpense(id);
      onDelete(REFRESH_PATTERNS.EXPENSES_AND_SETTLEMENT);
    } catch (err) {
      console.error('Error deleting expense:', err);
    }
  };

  return (
    <div className="card">
      <h2>📝 Expenses</h2>
      <div className="expenses-list">
        {expenses.length === 0 ? (
          <div className="empty-state">No expenses added yet</div>
        ) : (
          expenses.map((expense) => {
            const perUserAmount =
              (expense.amount / expense.split_between.length).toFixed(2);
            return (
              <div key={expense.id} className="expense-item">
                <div className="expense-item-header">
                  <span className="expense-description">
                    {expense.description}
                  </span>
                  <span className="expense-amount">
                    Rs {expense.amount.toFixed(2)}
                  </span>
                </div>
                <div className="expense-meta">
                  <div className="meta-item">
                    <strong>Paid by:</strong> {expense.paid_by}
                  </div>
                  <div className="meta-item">
                    <strong>Split between:</strong> {expense.split_between.join(', ')}
                  </div>
                  <div className="meta-item">
                    <strong>Per user:</strong> Rs {perUserAmount}
                  </div>
                  <div className="meta-item">
                    <strong>Date:</strong> {formatDate(expense.date)}
                  </div>
                </div>
                <button
                  className="delete-btn"
                  onClick={() => handleDelete(expense.id)}
                >
                  Delete
                </button>
              </div>
            );
          })
        )}
      </div>
    </div>
  );
}

export default ExpensesList;
