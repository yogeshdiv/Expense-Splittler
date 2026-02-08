from fastapi import APIRouter, HTTPException, Depends
from validation_models.models import ExpenseCreate, Expense, Settlement
from sqlalchemy.orm import Session
from db.models.expense import Expenses
from db.models.users import Users
from db.utils import get_db
from typing import List
from datetime import datetime

router = APIRouter()


@router.get("/expenses", response_model=List[Expense])
async def get_expenses(db: Session = Depends(get_db)):
    return db.query(Expenses).all()


@router.post("/expenses", response_model=Expense)
async def create_expense(expense: ExpenseCreate, db: Session = Depends(get_db)):
    """Create a new expense"""
    # Check if payer exists
    paid_by_user = db.query(Users).filter(Users.name == expense.paid_by).first()
    if not paid_by_user:
        raise HTTPException(status_code=400, detail="Payer not found in users list")

    if not expense.split_between:
        raise HTTPException(status_code=400, detail="Must split between at least one person")

    # Check if all split people exist
    split_people = db.query(Users).filter(
        Users.name.in_(expense.split_between)
    ).all()

    if len(split_people) != len(expense.split_between):
        raise HTTPException(400, "Some split people not found")

    # Create expense
    expense_date = datetime.strptime(expense.date, "%Y-%m-%d").date()

    new_expense = Expenses(
        description=expense.description,
        amount=expense.amount,
        paid_by_id=paid_by_user.id,
        date=expense_date
    )

    new_expense.split_between_users = split_people

    db.add(new_expense)
    db.commit()
    db.refresh(new_expense)

    return new_expense

@router.delete("/expenses/{expense_id}")
async def delete_expense(expense_id: int, db: Session = Depends(get_db)):
    """Delete an expense"""

    expense = db.query(Expenses).filter(Expenses.id == expense_id).first()
    if not expense:
        raise HTTPException(status_code=404, detail="Expense not found")

    db.delete(expense)
    db.commit()

    return {"message": "Expense deleted"}

@router.get("/settlement", response_model=List[Settlement])
async def get_settlement(db: Session = Depends(get_db)):
    """Get simplified settlement"""

    # Get all people
    all_people = db.query(Users).all()
    people_names = [p.name for p in all_people]

    if not people_names:
        return []

    # Calculate balances
    balances = {}
    for person_name in people_names:
        balances[person_name] = 0.0

    # Get all expenses
    expenses = db.query(Expenses).all()

    for expense in expenses:
        amount_per_person = expense.amount / len(expense.split_between_users)

        # Add money paid by this person
        balances[expense.paid_by_user.name] += expense.amount

        # Subtract money they should pay
        for person in expense.split_between_users:
            balances[person.name] -= amount_per_person

    # Simplify debts
    transactions = []

    # Separate debtors and creditors
    debtors = []
    creditors = []

    tolerance = 1e-9
    for person_name, balance in balances.items():
        if balance > tolerance:
            creditors.append({"name": person_name, "amount": balance})
        elif balance < -tolerance:
            debtors.append({"name": person_name, "amount": abs(balance)})

    # Match debtors with creditors
    while debtors and creditors:
        debtor = debtors[0]
        creditor = creditors[0]

        amount = min(debtor["amount"], creditor["amount"])

        transactions.append(Settlement(
            from_person=debtor["name"],
            to_person=creditor["name"],
            amount=round(amount, 2)
        ))

        debtor["amount"] -= amount
        creditor["amount"] -= amount

        if debtor["amount"] < tolerance:
            debtors.pop(0)
        if creditor["amount"] < tolerance:
            creditors.pop(0)
 
    return transactions
