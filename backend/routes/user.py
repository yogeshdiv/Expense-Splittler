from fastapi import APIRouter, HTTPException, Depends
from db.utils import get_db
from db.models.users import Users
from typing import List
from sqlalchemy.orm import Session
from validation_models.models import UserCreate, User

router = APIRouter()

@router.get("/users", response_model=List[str])
async def get_people(db: Session = Depends(get_db)):
    """Get all users"""
    people = db.query(Users).all()
    return [person.name for person in people]

@router.post("/users", response_model=str)
async def add_user(person: UserCreate, db: Session = Depends(get_db)):
    """Add a new user"""
    name = person.name.strip()
    
    if not name:
        raise HTTPException(status_code=400, detail="Name cannot be empty")
    
    existing_person = db.query(Users).filter(Users.name == name).first()
    if existing_person:
        raise HTTPException(status_code=400, detail="User already exists")
    
    new_person = Users(name=name)
    db.add(new_person)
    db.commit()
    db.refresh(new_person)
    
    return name

@router.delete("/users/{name}")
async def remove_user(name: str, db: Session = Depends(get_db)):
    """Remove a user"""
    person = db.query(Users).filter(Users.name == name).first()
    
    if not person:
        raise HTTPException(status_code=404, detail="User not found")
    
    db.delete(person)
    db.commit()
    
    return {"message": f"{name} removed"}
