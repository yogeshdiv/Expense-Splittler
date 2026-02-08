import React, { useState } from 'react';
import * as api from '../api';
import { REFRESH_PATTERNS } from '../utils';

function UserSection({ users, onUpdate }) {
  const [userName, setUserName] = useState('');
  const [error, setError] = useState('');

  const handleAddUser = async (e) => {
    e.preventDefault();
    setError('');

    const name = userName.trim();
    if (!name) {
      setError('Please enter a name');
      return;
    }

    try {
      await api.addUser(name);
      setUserName('');
      onUpdate(REFRESH_PATTERNS.USERS_ONLY);
    } catch (err) {
      setError(err.response?.data?.detail || 'Error adding user');
    }
  };

  const handleRemoveUser = async (name) => {
    try {
      await api.removeUser(name);
      onUpdate(REFRESH_PATTERNS.ALL);
    } catch (err) {
      console.error('Error removing user:', err);
    }
  };

  return (
    <div className="card">
      <h2>👥 Add Users</h2>
      <form onSubmit={handleAddUser}>
        <div className="form-group">
          <label htmlFor="userName">Friend's Name</label>
          <input
            type="text"
            id="userName"
            placeholder="e.g., Alice"
            value={userName}
            onChange={(e) => setUserName(e.target.value)}
            autoComplete="off"
          />
          {error && <div className="error">{error}</div>}
        </div>
        <button type="submit">Add User</button>
      </form>

      <div className="users-list">
        {users.length === 0 ? (
          <div className="empty-state">No users added yet</div>
        ) : (
          users.map((user) => (
            <div key={user} className="user-tag">
              {user}
              <span
                className="remove"
                onClick={() => handleRemoveUser(user)}
              >
                ✕
              </span>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

export default UserSection;
