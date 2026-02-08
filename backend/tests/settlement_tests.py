def test_no_users(db_session):
    result = get_settlement(db_session)
    assert result == []


def test_single_user_no_expense(db_session, create_user):
    create_user("A")
    result = get_settlement(db_session)
    assert result == []


def test_two_users_single_expense(db_session, create_user, create_expense):
    create_user("A")
    create_user("B")

    create_expense(
        paid_by="A",
        amount=100,
        split_between=["A", "B"]
    )

    result = get_settlement(db_session)

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

    result = get_settlement(db_session)

    assert len(result) == 2
    amounts = sorted([t.amount for t in result])
    assert amounts == [40, 40]


def test_balances_cancel_out(db_session, create_user, create_expense):
    create_user("A")
    create_user("B")

    create_expense("A", 100, ["A", "B"])
    create_expense("B", 100, ["A", "B"])

    result = get_settlement(db_session)
    assert result == []


def test_chain_simplification(db_session, create_user, create_expense):
    for name in ["A", "B", "C"]:
        create_user(name)

    create_expense("A", 90, ["A", "B", "C"])  # B,C owe A 30
    create_expense("B", 60, ["B", "C"])       # C owes B 30

    result = get_settlement(db_session)

    assert len(result) == 1
    t = result[0]
    assert t.from_person == "C"
    assert t.to_person == "A"
    assert t.amount == 30


def test_rounding(db_session, create_user, create_expense):
    for name in ["A", "B", "C"]:
        create_user(name)

    create_expense("A", 100, ["A", "B", "C"])

    result = get_settlement(db_session)

    for t in result:
        assert round(t.amount, 2) == t.amount


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
        payer = db_session.query(Users).filter_by(name=paid_by).first()
        split_users = db_session.query(Users).filter(
            Users.name.in_(split_between)
        ).all()

        expense = Expenses(
            description="test",
            amount=amount,
            paid_by_id=payer.id,
            split_between_users=split_users,
            date=date.today()
        )
        db_session.add(expense)
        db_session.commit()
    return _create
