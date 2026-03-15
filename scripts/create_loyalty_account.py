import json
import uuid

from app.client import client
from square.core.api_error import ApiError

# These values come from the controlled sandbox setup we created by hand.
PROGRAM_ID = "66d91e95-c079-49b0-bce6-8fd0677452b1"
CUSTOMER_ID = "J42RRWSJYDP85FKFD046MSRTV4"
PHONE_NUMBER = "+14255550101"


def create_loyalty_account() -> dict | None:
    """Create one loyalty account linked to the sandbox test customer."""
    try:
        result = client.loyalty.accounts.create(
            # Keep retries from accidentally creating duplicate loyalty accounts.
            idempotency_key=str(uuid.uuid4()),
            loyalty_account={
                "program_id": PROGRAM_ID,
                "customer_id": CUSTOMER_ID,
                "mapping": {
                    # Phone number is the core loyalty identity mapping.
                    "phone_number": PHONE_NUMBER,
                },
            },
        )
    except ApiError as error:
        print("Loyalty account creation failed.")
        print(error)
        return None

    if result.errors:
        print("Loyalty account creation failed.")
        print(result.errors)
        return None

    if result.loyalty_account is None:
        print("Loyalty account creation returned no loyalty account.")
        return None

    return result.loyalty_account.model_dump()


if __name__ == "__main__":
    loyalty_account = create_loyalty_account()
    if loyalty_account:
        print(json.dumps(loyalty_account, indent=2))
