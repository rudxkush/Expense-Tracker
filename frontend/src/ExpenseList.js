import React, { useState, useEffect } from 'react';

const ExpenseList = ({ refreshTrigger }) => {
  const [expenses, setExpenses] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('');
  const [sortByDate, setSortByDate] = useState(false);
  const [categories, setCategories] = useState([]);

  const fetchExpenses = async () => {
    setLoading(true);
    setError('');
    
    try {
      const { api } = await import('./api');
      const filters = {};
      
      if (categoryFilter) {
        filters.category = categoryFilter;
      }
      if (sortByDate) {
        filters.sort = 'date_desc';
      }
      
      const data = await api.getExpenses(filters);
      setExpenses(data);
      
      // Extract unique categories
      const uniqueCategories = [...new Set(data.map(expense => expense.category))];
      setCategories(uniqueCategories);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchExpenses();
  }, [refreshTrigger, categoryFilter, sortByDate]);

  const totalAmount = expenses.reduce((sum, expense) => sum + expense.amount_cents, 0) / 100;

  if (loading) {
    return <div>Loading expenses...</div>;
  }

  if (error) {
    return <div style={{ color: 'red' }}>Error: {error}</div>;
  }

  return (
    <div>
      <div style={{ marginBottom: '1rem', padding: '1rem', backgroundColor: '#f5f5f5' }}>
        <h2>Expenses</h2>
        
        <div style={{ marginBottom: '1rem' }}>
          <label style={{ marginRight: '1rem' }}>
            Filter by category: 
            <select 
              value={categoryFilter} 
              onChange={(e) => setCategoryFilter(e.target.value)}
              style={{ marginLeft: '0.5rem', padding: '0.25rem' }}
            >
              <option value="">All categories</option>
              {categories.map(category => (
                <option key={category} value={category}>{category}</option>
              ))}
            </select>
          </label>
          
          <label>
            <input
              type="checkbox"
              checked={sortByDate}
              onChange={(e) => setSortByDate(e.target.checked)}
              style={{ marginRight: '0.25rem' }}
            />
            Sort by date (newest first)
          </label>
        </div>
        
        <div style={{ fontWeight: 'bold', fontSize: '1.2em' }}>
          Total: ${totalAmount.toFixed(2)}
        </div>
      </div>

      {expenses.length === 0 ? (
        <div>No expenses found.</div>
      ) : (
        <table style={{ width: '100%', borderCollapse: 'collapse' }}>
          <thead>
            <tr style={{ backgroundColor: '#f0f0f0' }}>
              <th style={{ padding: '0.5rem', border: '1px solid #ddd', textAlign: 'left' }}>Date</th>
              <th style={{ padding: '0.5rem', border: '1px solid #ddd', textAlign: 'left' }}>Category</th>
              <th style={{ padding: '0.5rem', border: '1px solid #ddd', textAlign: 'left' }}>Description</th>
              <th style={{ padding: '0.5rem', border: '1px solid #ddd', textAlign: 'right' }}>Amount</th>
            </tr>
          </thead>
          <tbody>
            {expenses.map(expense => (
              <tr key={expense.id}>
                <td style={{ padding: '0.5rem', border: '1px solid #ddd' }}>{expense.date}</td>
                <td style={{ padding: '0.5rem', border: '1px solid #ddd' }}>{expense.category}</td>
                <td style={{ padding: '0.5rem', border: '1px solid #ddd' }}>{expense.description}</td>
                <td style={{ padding: '0.5rem', border: '1px solid #ddd', textAlign: 'right' }}>
                  ${(expense.amount_cents / 100).toFixed(2)}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      )}
    </div>
  );
};

export default ExpenseList;