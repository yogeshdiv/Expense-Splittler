from fastapi import APIRouter, Depends
from db.utils import get_db
from typing import List
from sqlalchemy.orm import Session
from validation_models.models import UserCreate, UserResponse
from services.user import get_all_users_service, add_user_service, delete_user_service

router = APIRouter()

@router.get("/users", response_model=List[str])
def get_people(db: Session = Depends(get_db)):
    """Get all users"""
    people = get_all_users_service(db)
    return [person.name for person in people]

@router.post("/users", response_model=UserResponse)
def add_user(person: UserCreate, db: Session = Depends(get_db)):
    """Add a new user"""
    return add_user_service(person.name, db)

@router.delete("/users/{name}", status_code=204)
def remove_user(name: str, db: Session = Depends(get_db)):
    """Remove a user"""
    delete_user_service(name, db)
