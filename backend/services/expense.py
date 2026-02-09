from datetime import datetime
from sqlalchemy.orm import Session
from fastapi import HTTPException

from db.models.users import Users
from db.models.expense import Expenses
from validation_models.models import Expense, ExpenseCreate


def create_expense_service(expense_data: ExpenseCreate, db: Session) -> Expense:
    paid_by_user = db.query(Users).filter(
        Users.name == expense_data.paid_by
    ).first()

    if not paid_by_user:
        raise HTTPException(400, "Payer not found in users list")

    split_people = db.query(Users).filter(
        Users.name.in_(expense_data.split_between)
    ).all()

    if len(split_people) != len(expense_data.split_between):
        raise HTTPException(400, "Some split people not found")

    expense_date = datetime.strptime(
        expense_data.date, "%Y-%m-%d"
    ).date()

    new_expense = Expenses(
        description=expense_data.description,
        amount=expense_data.amount,
        paid_by_id=paid_by_user.id,
        date=expense_date,
    )

    new_expense.split_between_users = split_people
    db.add(new_expense)

    # update balances
    share = expense_data.amount / len(split_people)
    paid_by_user.balance += expense_data.amount

    for user in split_people:
        user.balance -= share

    db.commit()
    db.refresh(new_expense)

    return new_expense

def delete_expense_service(expense_id: int, db: Session):
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
