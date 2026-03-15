import json
import uuid

from app.client import client
from square.core.api_error import ApiError

LOYALTY_ACCOUNT_ID = "ad026a62-f825-4927-98a1-4e093bc9ea6f"
LOYALTY_PROGRAM_ID = "66d91e95-c079-49b0-bce6-8fd0677452b1"
ORDER_ID = "t4uhAZfm9elAobsgz3aGguFsCPRZY"
LOCATION_ID = "LT2KY461H6N41"


def accumulate_loyalty_points() -> dict | None:
    """Accumulate loyalty points for the completed sandbox order."""
    try:
        result = client.loyalty.accounts.accumulate_points(
            LOYALTY_ACCOUNT_ID,
            idempotency_key=str(uuid.uuid4()),
            location_id=LOCATION_ID,
            accumulate_points={
                "loyalty_program_id": LOYALTY_PROGRAM_ID,
                "order_id": ORDER_ID,
            },
        )
    except ApiError as error:
        print("Loyalty points accumulation failed.")
        print(error)
        return None

    if result.errors:
        print("Loyalty points accumulation failed.")
        print(result.errors)
        return None

    if result.events:
        return {
            "events": [event.model_dump() for event in result.events],
        }

    if result.event is not None:
        return result.event.model_dump()

    print("Loyalty points accumulation returned no qualifying loyalty events.")
    print("This can happen when the purchase does not qualify for points.")
    return None


if __name__ == "__main__":
    event = accumulate_loyalty_points()
    if event:
        print(json.dumps(event, indent=2))
