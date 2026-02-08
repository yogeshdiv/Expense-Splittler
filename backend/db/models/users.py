from sqlalchemy import String, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.models.expense_users import expense_split
from db.connection import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(
        String,
        unique=True,
        index=True,
        nullable=False,
    )
    balance: Mapped[float] = mapped_column(Float, default=0.0)

    expenses_paid: Mapped[list["Expenses"]] = relationship(
        back_populates="paid_by_user"
    )

    expenses_split: Mapped[list["Expenses"]] = relationship(
        secondary=expense_split,
        back_populates="split_between_users",
    )