from typing import List
from pydantic import BaseModel
from datetime import date


class UserCreate(BaseModel):
    name: str

class UserResponse(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class ExpenseCreate(BaseModel):
    description: str
    amount: float
    paid_by: str
    split_between: List[str]
    date: str

class Expense(BaseModel):
    id: int
    description: str
    amount: float
    paid_by: str
    split_between: List[str]
    date: date

    class Config:
        orm_mode = True

class Settlement(BaseModel):
    from_person: str
    to_person: str
    amount: float