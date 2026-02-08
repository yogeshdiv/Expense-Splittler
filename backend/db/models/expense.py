from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship
from db.connection import Base
from db.models.expense_users import expense_split


class Expenses(Base):
    __tablename__ = "expenses"

    id = Column(Integer, primary_key=True, index=True)
    description = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    paid_by_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    date = Column(Date, nullable=False)

    # Relationships
    paid_by_user = relationship(
        "Users",
        back_populates="expenses_paid",
        foreign_keys=[paid_by_id],
    )

    split_between_users = relationship(
        "Users",
        secondary=expense_split,
        back_populates="expenses_split",
    )

    @property
    def paid_by(self) -> str:
        return self.paid_by_user.name

    @property
    def split_between(self) -> list[str]:
        return [user.name for user in self.split_between_users]
