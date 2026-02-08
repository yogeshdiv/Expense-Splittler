    
from validation_models.models import Settlement
from sqlalchemy.orm import Session
from db.models.users import Users

def calculate_settlement(db: Session) -> list[Settlement]:
    users = db.query(Users).all()

    tolerance = 1e-9
    people_who_should_receive = []
    people_who_should_pay = []

    # Step 1: Separate users based on balance
    for user in users:
        if user.balance > tolerance:
            people_who_should_receive.append(
                {"name": user.name, "amount": user.balance}
            )
        elif user.balance < -tolerance:
            people_who_should_pay.append(
                {"name": user.name, "amount": -user.balance}
            )

    settlements = []
    payer_index = 0
    receiver_index = 0

    # Step 2: Match payers with receivers
    while (
        payer_index < len(people_who_should_pay)
        and receiver_index < len(people_who_should_receive)
    ):
        payer = people_who_should_pay[payer_index]
        receiver = people_who_should_receive[receiver_index]

        settlement_amount = min(payer["amount"], receiver["amount"])

        settlements.append(
            Settlement(
                from_person=payer["name"],
                to_person=receiver["name"],
                amount=round(settlement_amount, 2),
            )
        )

        payer["amount"] -= settlement_amount
        receiver["amount"] -= settlement_amount

        if payer["amount"] < tolerance:
            payer_index += 1

        if receiver["amount"] < tolerance:
            receiver_index += 1

    return settlements
