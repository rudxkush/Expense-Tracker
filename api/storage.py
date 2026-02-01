import json
import os

STORAGE_FILE = '/tmp/expenses.json'

def load_expenses():
    if os.path.exists(STORAGE_FILE):
        with open(STORAGE_FILE, 'r') as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    with open(STORAGE_FILE, 'w') as f:
        json.dump(expenses, f)

def add_expense(expense_data):
    expenses = load_expenses()
    
    # Check for existing expense with same idempotency key
    existing = next((e for e in expenses if e.get('idempotency_key') == expense_data.get('idempotency_key')), None)
    if existing:
        return existing
    
    # Create new expense
    expense = {
        'id': len(expenses) + 1,
        'idempotency_key': expense_data.get('idempotency_key'),
        'amount_cents': int(expense_data['amount'] * 100),
        'category': expense_data['category'],
        'description': expense_data['description'],
        'date': expense_data['date'],
        'created_at': expense_data.get('created_at')
    }
    
    expenses.append(expense)
    save_expenses(expenses)
    return expense

def get_expenses(category=None, sort_param=None):
    expenses = load_expenses()
    
    # Filter by category
    if category:
        expenses = [e for e in expenses if e.get('category') == category]
    
    # Sort expenses
    if sort_param == 'date_desc':
        expenses = sorted(expenses, key=lambda x: x.get('date', ''), reverse=True)
    else:
        expenses = sorted(expenses, key=lambda x: x.get('created_at', ''), reverse=True)
    
    return expenses