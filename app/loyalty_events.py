import json

from client import client


def search_loyalty_events() -> list[dict]:
    cursor = None
    records = []

    while True:
        results = client.loyalty.search_events(cursor=cursor)

        if results.errors:
            print("Searching loyalty events failed.")
            print(results.errors)
            break

        if not results.events:
            break

        for event in results.events:
            records.append(
                {
                    "id": event.id,
                    "loyalty_account_id": event.loyalty_account_id,
                    "event_type": event.type,
                    "created_at": event.created_at,
                }
            )

        cursor = results.cursor

        if cursor is None:
            break

    return records


if __name__ == "__main__":
    records = search_loyalty_events()
    print(json.dumps(records, indent=2))
