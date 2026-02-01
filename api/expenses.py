from http.server import BaseHTTPRequestHandler
import json
from datetime import datetime
import os

# Inline storage functions
def load_expenses():
    storage_file = '/tmp/expenses.json'
    if os.path.exists(storage_file):
        with open(storage_file, 'r') as f:
            return json.load(f)
    return []

def save_expenses(expenses):
    storage_file = '/tmp/expenses.json'
    with open(storage_file, 'w') as f:
        json.dump(expenses, f)

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        expenses = load_expenses()
        
        # Check for existing expense with same idempotency key
        existing = next((e for e in expenses if e.get('idempotency_key') == data.get('idempotency_key')), None)
        if existing:
            expense = existing
        else:
            # Create new expense
            expense = {
                'id': len(expenses) + 1,
                'idempotency_key': data.get('idempotency_key'),
                'amount_cents': int(data['amount'] * 100),
                'category': data['category'],
                'description': data['description'],
                'date': data['date'],
                'created_at': datetime.now().isoformat()
            }
            expenses.append(expense)
            save_expenses(expenses)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(json.dumps(expense).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()