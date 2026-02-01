from http.server import BaseHTTPRequestHandler
import json
import sqlite3
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        data = json.loads(post_data.decode('utf-8'))
        
        # Create in-memory database
        conn = sqlite3.connect(':memory:')
        cursor = conn.cursor()
        
        # Create table
        cursor.execute('''
            CREATE TABLE expenses (
                id INTEGER PRIMARY KEY,
                idempotency_key TEXT UNIQUE,
                amount_cents INTEGER,
                category TEXT,
                description TEXT,
                date TEXT,
                created_at TEXT
            )
        ''')
        
        # Create expense
        expense = {
            'id': 1,
            'amount_cents': int(data['amount'] * 100),
            'category': data['category'],
            'description': data['description'],
            'date': data['date'],
            'created_at': datetime.now().isoformat()
        }
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(json.dumps(expense).encode())
        
        conn.close()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()