// Use relative URLs for Vercel deployment, fallback to localhost for development
const API_BASE = process.env.NODE_ENV === 'production' ? '/api' : 'http://localhost:8000';

// Generate unique idempotency key
const generateIdempotencyKey = () => {
  return `${Date.now()}-${Math.random().toString(36).substr(2, 9)}`;
};

export const api = {
  async createExpense(expenseData) {
    const idempotencyKey = generateIdempotencyKey();
    
    try {
      const response = await fetch(`${API_BASE}/expenses`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          ...expenseData,
          idempotency_key: idempotencyKey
        }),
      });

      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('Create expense error:', error);
      throw new Error('Failed to create expense');
    }
  },

  async getExpenses(filters = {}) {
    const params = new URLSearchParams();
    
    if (filters.category) {
      params.append('category', filters.category);
    }
    if (filters.sort) {
      params.append('sort', filters.sort);
    }

    try {
      const response = await fetch(`${API_BASE}/list?${params}`);
      
      if (!response.ok) {
        throw new Error(`HTTP ${response.status}`);
      }

      return response.json();
    } catch (error) {
      console.error('Get expenses error:', error);
      throw new Error('Failed to fetch expenses');
    }
  }
};