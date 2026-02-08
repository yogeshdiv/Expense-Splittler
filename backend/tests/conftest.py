import sys
import os
from datetime import date

# Set dummy DATABASE_URL before importing db modules
os.environ.setdefault("DATABASE_URL", "sqlite:///:memory:")

import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from db.connection import Base
from tests.test_db import TestingSessionLocal, engine
from db.models.users import Users
from services.expense import create_expense_service
from validation_models.models import ExpenseCreate


@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)

    session = TestingSessionLocal()
    yield session

    session.close()
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def create_user(db_session):
    def _create(name):
        user = Users(name=name)
        db_session.add(user)
        db_session.commit()
    return _create


@pytest.fixture
def create_expense(db_session):
    def _create(paid_by, amount, split_between):
        expense_data = ExpenseCreate(
            description="test",
            amount=amount,
            paid_by=paid_by,
            split_between=split_between,
            date=date.today().strftime("%Y-%m-%d")
        )
        create_expense_service(expense_data, db_session)
    return _create
