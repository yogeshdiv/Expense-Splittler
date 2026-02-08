from fastapi import APIRouter, HTTPException, Depends
from validation_models.models import ExpenseCreate, Expense, Settlement
from sqlalchemy.orm import Session
from db.models.expense import Expenses
from db.utils import get_db
from typing import List
from services.settlement import calculate_settlement
from services.expense import create_expense_service

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

    expense = db.query(Expenses).filter(Expenses.id == expense_id).first()
    if not expense:
        raise HTTPException(404, "Expense not found")

    split_users = expense.split_between_users
    share = expense.amount / len(split_users)

    expense.paid_by_user.balance -= expense.amount

    for user in split_users:
        user.balance += share

    db.delete(expense)
    db.commit()


@router.get("/settlement", response_model=List[Settlement])
def get_settlement(db: Session = Depends(get_db)):
    return calculate_settlement(db)
