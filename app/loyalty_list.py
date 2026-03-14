"""
loyalty_accounts_search.py

Fetch all loyalty accounts from Square using cursor pagination
and print the loyalty account ID and associated customer ID.
"""

import json

from client import client


def loyalty_accounts_search() -> list[dict]:
    """Fetch loyalty account records and print their IDs."""
    cursor = None
    records = []
    count = 0

    while True:
        result = client.loyalty.accounts.search(cursor=cursor)
        if result.errors:
            print("Loyalty accounts search failed.")
            print(result.errors)
            break

        if result.loyalty_accounts is None:
            print(f"No loyalty accounts returned. Stopping after {count} accounts.")
            break

        for acct in result.loyalty_accounts:
            loyalty_id = acct.id
            customer_id = acct.customer_id or "NO_CUSTOMER"

            records.append(
                {
                    "loyalty_account_id": loyalty_id,
                    "customer_id": customer_id,
                }
            )

            count += 1

            print(f"loyalty_id: {loyalty_id}, customer_id: {customer_id}")
            print(f"processed {count} accounts")

        cursor = result.cursor

        if cursor is None:
            break

    return records


if __name__ == "__main__":
    records = loyalty_accounts_search()
    print(json.dumps(records, indent=2))
