import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from services.settlement import calculate_settlement


def test_no_users(db_session):
    result = calculate_settlement(db_session)
    assert result == []


def test_single_user_no_expense(db_session, create_user):
    create_user("A")
    result = calculate_settlement(db_session)
    assert result == []


def test_two_users_single_expense(db_session, create_user, create_expense):
    create_user("A")
    create_user("B")

    create_expense(
        paid_by="A",
        amount=100,
        split_between=["A", "B"]
    )

    result = calculate_settlement(db_session)

    assert len(result) == 1
    t = result[0]
    assert t.from_person == "B"
    assert t.to_person == "A"
    assert t.amount == 50


def test_three_users_one_payer(db_session, create_user, create_expense):
    for name in ["A", "B", "C"]:
        create_user(name)

    create_expense(
        paid_by="A",
        amount=120,
        split_between=["A", "B", "C"]
    )

    result = calculate_settlement(db_session)

    assert len(result) == 2
    amounts = sorted([t.amount for t in result])
    assert amounts == [40, 40]


def test_balances_cancel_out(db_session, create_user, create_expense):
    create_user("A")
    create_user("B")

    create_expense("A", 100, ["A", "B"])
    create_expense("B", 100, ["A", "B"])

    result = calculate_settlement(db_session)
    assert result == []


def test_chain_simplification(db_session, create_user, create_expense):
    for name in ["A", "B", "C"]:
        create_user(name)

    create_expense("A", 90, ["A", "B", "C"])  # B,C owe A 30
    create_expense("B", 60, ["B", "C"])       # C owes B 30

    result = calculate_settlement(db_session)

    assert len(result) == 1
    t = result[0]
    assert t.from_person == "C"
    assert t.to_person == "A"
    assert t.amount == 60


def test_rounding(db_session, create_user, create_expense):
    for name in ["A", "B", "C"]:
        create_user(name)

    create_expense("A", 100, ["A", "B", "C"])

    result = calculate_settlement(db_session)

    for t in result:
        assert round(t.amount, 2) == t.amount
