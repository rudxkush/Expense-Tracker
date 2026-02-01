import React, { useState } from 'react';
import ExpenseForm from './ExpenseForm';
import ExpenseList from './ExpenseList';

function App() {
  const [refreshTrigger, setRefreshTrigger] = useState(0);

  const handleExpenseAdded = () => {
    setRefreshTrigger(prev => prev + 1);
  };

  return (
    <div style={{ maxWidth: '800px', margin: '0 auto', padding: '1rem' }}>
      <h1>Expense Tracker</h1>
      <ExpenseForm onExpenseAdded={handleExpenseAdded} />
      <ExpenseList refreshTrigger={refreshTrigger} />
    </div>
  );
}

export default App;