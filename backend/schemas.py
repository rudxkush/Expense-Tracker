from pydantic import BaseModel, validator, Field
from datetime import date, datetime
from typing import Optional

class ExpenseCreate(BaseModel):
    idempotency_key: str
    amount: float  # Frontend sends as float, we convert to cents
    category: str
    description: str
    date: date
    
    @validator('amount')
    def amount_must_be_positive(cls, v):
        if v <= 0:
            raise ValueError('Amount must be greater than 0')
        return v

class ExpenseResponse(BaseModel):
    id: int
    amount_cents: int
    category: str
    description: str
    date: date
    created_at: datetime
    
    class Config:
        from_attributes = True