from typing import List
from pydantic import BaseModel
from datetime import date


# Pydantic Models
class UserCreate(BaseModel):
    name: str

class User(UserCreate):
    id: int
    
    class Config:
        from_attributes = True

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