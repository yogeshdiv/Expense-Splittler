from fastapi import APIRouter, HTTPException, Depends
from validation_models.models import ExpenseCreate, Expense, Settlement
from sqlalchemy.orm import Session
from db.models.expense import Expenses
from db.utils import get_db
from typing import List
from services.settlement import calculate_settlement
from services.expense import create_expense_service, delete_expense_service

router = APIRouter()


@router.get("/expenses", response_model=List[Expense])
def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expenses).all()

@router.post("/expenses", response_model=Expense)
def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """Create a new expense"""
    return create_expense_service(expense, db)

@router.delete("/expenses/{expense_id}", status_code=204)
def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Delete an expense and revert balances"""

    delete_expense_service(expense_id, db)


@router.get("/settlement", response_model=List[Settlement])
def get_settlement(db: Session = Depends(get_db)):
    return calculate_settlement(db)
