from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from db.models.expense_users import expense_split
from db.connection import Base

class Users(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    
    expenses_paid = relationship("Expenses", back_populates="paid_by_user")
    expenses_split = relationship(
        "Expenses",
        secondary=expense_split,
        back_populates="split_between_users"
    )
