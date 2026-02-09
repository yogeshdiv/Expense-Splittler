from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import select, exists

from db.models.users import Users
from db.models.expense import Expenses
from db.models.expense_users import expense_split


def get_all_users_service(db: Session):
    return db.query(Users).all()


def add_user_service(name: str, db: Session) -> Users:
    name = name.strip()

    if not name:
        raise HTTPException(400, "Name cannot be empty")

    stmt = select(exists().where(Users.name == name))
    user_exists = db.execute(stmt).scalar()

    if user_exists:
        raise HTTPException(409, "User already exists")

    new_person = Users(name=name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)

    return new_person


def delete_user_service(name: str, db: Session):
    person = db.query(Users).filter(Users.name == name).first()

    if not person:
        raise HTTPException(404, "User not found")

    paid_exists = db.execute(
        select(exists().where(Expenses.paid_by_id == person.id))
    ).scalar()

    split_exists = db.execute(
        select(exists().where(expense_split.c.user_id == person.id))
    ).scalar()

    if paid_exists or split_exists:
        raise HTTPException(
            400,
            "User cannot be deleted because they are associated with existing expenses",
        )

    db.delete(person)
    db.commit()
