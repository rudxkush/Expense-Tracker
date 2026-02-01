from fastapi import FastAPI, Depends, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import Optional, List

from .models import Expense, get_db, create_tables
from .schemas import ExpenseResponse

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()

@app.get("/")
def handler(
    category: Optional[str] = Query(None),
    sort: Optional[str] = Query(None),
    db: Session = Depends(get_db)
):
    query = db.query(Expense)
    
    if category:
        query = query.filter(Expense.category == category)
    
    if sort == "date_desc":
        query = query.order_by(Expense.date.desc())
    else:
        query = query.order_by(Expense.created_at.desc())
    
    expenses = query.all()
    return [ExpenseResponse.from_orm(expense).dict() for expense in expenses]