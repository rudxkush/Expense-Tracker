from http.server import BaseHTTPRequestHandler
import json
import os
from urllib.parse import parse_qs, urlparse

# Inline storage functions
def load_expenses():
    storage_file = '/tmp/expenses.json'
    if os.path.exists(storage_file):
        with open(storage_file, 'r') as f:
            return json.load(f)
    return []

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        category = params.get('category', [None])[0]
        sort_param = params.get('sort', [None])[0]
        
        # Load expenses from shared storage
        expenses = load_expenses()
        
        # Filter by category
        if category:
            expenses = [e for e in expenses if e.get('category') == category]
        
        # Sort expenses
        if sort_param == 'date_desc':
            expenses = sorted(expenses, key=lambda x: x.get('date', ''), reverse=True)
        else:
            expenses = sorted(expenses, key=lambda x: x.get('created_at', ''), reverse=True)
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(json.dumps(expenses).encode())
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()