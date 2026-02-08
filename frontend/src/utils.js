// Common utility functions
export const formatDate = (dateStr) => {
  const date = new Date(dateStr + 'T00:00:00');
  return date.toLocaleDateString('en-IN', {
    year: 'numeric',
    month: 'short',
    day: 'numeric',
  });
};

// Common refresh patterns
export const REFRESH_PATTERNS = {
  ALL: { users: true, expenses: true, settlement: true },
  USERS_ONLY: { users: true, expenses: false, settlement: false },
  EXPENSES_AND_SETTLEMENT: { users: false, expenses: true, settlement: true },
};
