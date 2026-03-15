import json
import uuid

from app.client import client
from square.core.api_error import ApiError

ORDER_ID = "t4uhAZfm9elAobsgz3aGguFsCPRZY"
CUSTOMER_ID = "J42RRWSJYDP85FKFD046MSRTV4"
LOCATION_ID = "LT2KY461H6N41"
AMOUNT_MONEY = {
    "amount": 775,
    "currency": "USD",
}


def create_payment() -> dict | None:
    """Create a sandbox cash payment for the current test order."""
    try:
        result = client.payments.create(
            source_id="CASH",
            idempotency_key=str(uuid.uuid4()),
            amount_money=AMOUNT_MONEY,
            order_id=ORDER_ID,
            customer_id=CUSTOMER_ID,
            location_id=LOCATION_ID,
            cash_details={
                "buyer_supplied_money": AMOUNT_MONEY,
            },
            note="Sandbox payment for loyalty order testing.",
        )
    except ApiError as error:
        print("Payment creation failed.")
        print(error)
        return None

    if result.errors:
        print("Payment creation failed.")
        print(result.errors)
        return None

    if result.payment is None:
        print("Payment creation returned no payment.")
        return None

    return result.payment.model_dump()


if __name__ == "__main__":
    payment = create_payment()
    if payment:
        print(json.dumps(payment, indent=2))
