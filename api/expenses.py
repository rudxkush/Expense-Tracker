from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging

from .models import Expense, get_db, create_tables
from .schemas import ExpenseCreate, ExpenseResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()

@app.post("/")
def handler(expense: ExpenseCreate, db: Session = Depends(get_db)):
    existing = db.query(Expense).filter(Expense.idempotency_key == expense.idempotency_key).first()
    if existing:
        return ExpenseResponse.from_orm(existing).dict()
    
    amount_cents = int(expense.amount * 100)
    db_expense = Expense(
        idempotency_key=expense.idempotency_key,
        amount_cents=amount_cents,
        category=expense.category,
        description=expense.description,
        date=expense.date
    )
    
    try:
        db.add(db_expense)
        db.commit()
        db.refresh(db_expense)
        return ExpenseResponse.from_orm(db_expense).dict()
    except IntegrityError:
        db.rollback()
        existing = db.query(Expense).filter(Expense.idempotency_key == expense.idempotency_key).first()
        if existing:
            return ExpenseResponse.from_orm(existing).dict()
        raise HTTPException(status_code=500, detail="Failed to create expense")