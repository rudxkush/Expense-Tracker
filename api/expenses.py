from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
import logging

from .models import Expense, get_db, create_tables
from .schemas import ExpenseCreate, ExpenseResponse

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

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

@app.post("/", response_model=ExpenseResponse)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """Create expense with idempotency protection"""
    
    # Check if expense with this idempotency key already exists
    existing = db.query(Expense).filter(Expense.idempotency_key == expense.idempotency_key).first()
    if existing:
        logger.info(f"Returning existing expense for idempotency key: {expense.idempotency_key}")
        return ExpenseResponse.from_orm(existing)
    
    # Convert amount to cents for storage
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
        logger.info(f"Created new expense with id: {db_expense.id}")
        return ExpenseResponse.from_orm(db_expense)
    except IntegrityError:
        db.rollback()
        # Race condition: another request created the same idempotency key
        existing = db.query(Expense).filter(Expense.idempotency_key == expense.idempotency_key).first()
        if existing:
            logger.info(f"Race condition handled for idempotency key: {expense.idempotency_key}")
            return ExpenseResponse.from_orm(existing)
        raise HTTPException(status_code=500, detail="Failed to create expense")