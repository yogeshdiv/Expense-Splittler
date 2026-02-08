from datetime import date
from sqlalchemy import ForeignKey, Date, String, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship

from db.connection import Base
from db.models.expense_users import expense_split


class Expenses(Base):
    __tablename__ = "expenses"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    description: Mapped[str] = mapped_column(String, nullable=False)
    amount: Mapped[float] = mapped_column(Float, nullable=False)

    paid_by_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"),
        nullable=False,
    )

    date: Mapped[date] = mapped_column(Date, nullable=False)

    paid_by_user: Mapped["Users"] = relationship(
        back_populates="expenses_paid",
        foreign_keys=[paid_by_id],
    )

    split_between_users: Mapped[list["Users"]] = relationship(
        secondary=expense_split,
        back_populates="expenses_split",
    )

    @property
    def paid_by(self) -> str:
        return self.paid_by_user.name

    @property
    def split_between(self) -> list[str]:
        return [user.name for user in self.split_between_users]
