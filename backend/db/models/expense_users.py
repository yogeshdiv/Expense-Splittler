
from sqlalchemy import Table
from sqlalchemy import Column, Integer, ForeignKey
from db.connection import Base

expense_split = Table(
    "expense_split",
    Base.metadata,
    Column("expense_id", Integer, ForeignKey("expenses.id", ondelete="CASCADE")),
    Column("user_id", Integer, ForeignKey("users.id", ondelete="CASCADE")),
)