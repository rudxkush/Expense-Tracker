from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List

from .models import Expense, get_db, create_tables
from .schemas import ExpenseResponse

app = FastAPI()

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
create_tables()

@app.get("/", response_model=List[ExpenseResponse])
def get_expenses(
    category: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    """Get expenses with optional filtering and sorting"""
    
    query = db.query(Expense)
    
    # Filter by category if provided
    if category:
        query = query.filter(Expense.category == category)
    
    # Sort by date if requested
    if sort == "date_desc":
        query = query.order_by(Expense.date.desc())
    else:
        query = query.order_by(Expense.created_at.desc())
    
    expenses = query.all()
    return [ExpenseResponse.from_orm(expense) for expense in expenses]