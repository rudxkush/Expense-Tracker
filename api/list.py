from http.server import BaseHTTPRequestHandler
import json
import sqlite3
from urllib.parse import parse_qs, urlparse
from datetime import datetime

class handler(BaseHTTPRequestHandler):
    def do_GET(self):
        # Parse query parameters
        parsed_url = urlparse(self.path)
        params = parse_qs(parsed_url.query)
        category = params.get('category', [None])[0]
        sort_param = params.get('sort', [None])[0]
        
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
        
        # Return empty list for now (data doesn't persist in serverless)
        expenses = []
        
        self.send_response(200)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()
        
        self.wfile.write(json.dumps(expenses).encode())
        
        conn.close()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()