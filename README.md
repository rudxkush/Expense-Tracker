# Expense Tracker

A minimal but production-minded full-stack expense tracking application built with FastAPI and React.

## Architecture Overview

```
expense-tracker/
├── backend/
│   ├── main.py          # FastAPI application with endpoints
│   ├── models.py        # SQLAlchemy database models
│   ├── schemas.py       # Pydantic request/response schemas
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.js       # Main React component
│   │   ├── ExpenseForm.js # Form component with validation
│   │   ├── ExpenseList.js # List component with filtering
│   │   ├── api.js       # API service layer
│   │   └── index.js     # React entry point
│   ├── public/index.html
│   └── package.json
└── README.md
```

## Key Design Decisions

### Backend Architecture

**FastAPI Choice**: Selected for its automatic OpenAPI documentation, built-in validation, and excellent async support for future scaling.

**SQLite Database**: Chosen for simplicity and zero-configuration deployment. File-based persistence ensures data survives restarts without requiring external database setup.

**Money Handling**: All monetary values stored as integers (cents) to avoid floating-point precision issues. The API accepts floats for convenience but immediately converts to cents.

**Idempotency Implementation**: 
- Each request includes a unique `idempotency_key`
- Database enforces uniqueness constraint on this key
- Duplicate requests return the original expense instead of creating duplicates
- Race conditions handled with try/catch on IntegrityError

### Frontend Architecture

**React with Functional Components**: Modern React patterns with hooks for state management. No external state management library needed for this scope.

**API Service Layer**: Centralized API calls in `api.js` with proper error handling and automatic idempotency key generation.

**Form Reliability**:
- Submit button disabled during requests
- Form validation prevents invalid submissions
- Error states clearly communicated to user
- Automatic form reset on successful submission

### Data Model

```sql
CREATE TABLE expenses (
    id INTEGER PRIMARY KEY,
    idempotency_key TEXT UNIQUE NOT NULL,
    amount_cents INTEGER NOT NULL,
    category TEXT NOT NULL,
    description TEXT NOT NULL,
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

## Reliability Features

### Idempotency Protection
- Client generates unique keys for each submission attempt
- Server checks for existing expenses with same key before creating
- Race conditions handled at database level with unique constraints
- Returns original expense for duplicate keys

### Error Handling
- Network failures gracefully handled with user feedback
- Form validation prevents invalid data submission
- Loading states prevent user confusion during slow requests
- Server-side validation as final safety net

### Money Precision
- All amounts stored as integers (cents) to avoid floating-point errors
- Conversion handled transparently in API layer
- Display formatting consistent throughout application

## Deployment

### Vercel Deployment
This application is configured for deployment on Vercel with:
- React frontend as static site
- FastAPI backend as serverless functions
- Automatic CORS handling

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions.

### Quick Deploy to Vercel
1. Push code to GitHub repository
2. Connect repository to Vercel
3. Deploy with default settings
4. API will be available at `/api/expenses` and `/api/list`

## Running the Application

### Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Server runs on http://localhost:8000

### Frontend
```bash
cd frontend
npm install
npm start
```
Application runs on http://localhost:3000

## API Endpoints

### POST /expenses
Creates a new expense with idempotency protection.

**Request Body:**
```json
{
  "idempotency_key": "unique-key-123",
  "amount": 25.50,
  "category": "Food",
  "description": "Lunch",
  "date": "2024-01-15"
}
```

### GET /expenses
Retrieves expenses with optional filtering and sorting.

**Query Parameters:**
- `category`: Filter by category name
- `sort=date_desc`: Sort by date, newest first

## Trade-offs and Limitations

### Chosen Trade-offs
1. **SQLite over PostgreSQL**: Simpler deployment but limited concurrent write performance
2. **No authentication**: Reduces complexity but limits production readiness
3. **Client-side filtering backup**: Server-side filtering implemented, but client could cache for better UX
4. **Minimal styling**: Focus on functionality over aesthetics

### Future Enhancements
- Database migration system for schema changes
- Pagination for large expense lists
- Bulk operations with batch idempotency
- Enhanced error recovery and retry logic
- Comprehensive test suite
- Docker containerization

## Testing Idempotency

A basic test can be run by making multiple POST requests with the same idempotency key:

```bash
# First request - creates expense
curl -X POST http://localhost:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"idempotency_key":"test-123","amount":10.50,"category":"Test","description":"Test expense","date":"2024-01-15"}'

# Second request - returns same expense
curl -X POST http://localhost:8000/expenses \
  -H "Content-Type: application/json" \
  -d '{"idempotency_key":"test-123","amount":99.99,"category":"Different","description":"Different data","date":"2024-01-16"}'
```

Both requests should return the same expense ID and original data.