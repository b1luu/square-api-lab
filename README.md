# Square OAuth Lab

Small Python project for learning the Square API and building safe, readable
data extraction scripts.

## Purpose

This repository is currently focused on one read-only workflow:

- connect to the Square Sandbox API
- fetch loyalty accounts with cursor pagination
- extract the loyalty account ID and associated customer ID
- return the results as structured Python data
- print the results as formatted JSON for inspection

The longer-term direction is to expand this into additional Square domains such
as customers and orders while keeping the code easy to review and safe to run.

The repository also now includes a small `scripts/` area for creating controlled
Sandbox test data. These scripts are useful when a fresh sandbox account has no
customers, loyalty accounts, or loyalty activity yet.

## Current Scope

The project currently includes:

- configuration loading from environment variables
- centralized Square client creation
- loyalty account retrieval with pagination
- loyalty event retrieval and raw payload inspection
- sandbox customer creation
- sandbox loyalty account creation
- loyalty program ID lookup
- basic API error handling
- simple structured output for reuse in later exports or joins

The `app/` folder is intentionally read-focused. The `scripts/` folder is used
for controlled sandbox setup tasks.

## Project Structure

```text
square-oauth-lab/
├── .env.example
├── .gitignore
├── README.md
├── requirements.txt
├── pyproject.toml
├── app/
│   ├── __init__.py
│   ├── config.py
│   ├── client.py
│   ├── loyalty_events.py
│   └── loyalty_list.py
└── scripts/
    ├── __init__.py
    ├── accumulate_loyalty_points.py
    ├── create_customer.py
    ├── create_loyalty_account.py
    ├── create_order.py
    ├── create_payment.py
    ├── get_loyalty_program.py
    ├── list_catalog_items.py
    └── list_catalog_metadata.py
```

File responsibilities:

- `app/config.py`: loads and validates required environment variables
- `app/client.py`: creates the Square client
- `app/loyalty_list.py`: fetches loyalty account data and prints JSON output
- `app/loyalty_events.py`: fetches loyalty event data and helps inspect raw event payloads
- `scripts/accumulate_loyalty_points.py`: applies loyalty point accrual to the completed sandbox order
- `scripts/create_customer.py`: creates a controlled sandbox customer for testing
- `scripts/get_loyalty_program.py`: retrieves the current seller loyalty program ID
- `scripts/create_loyalty_account.py`: creates a loyalty account linked to the sandbox test customer
- `scripts/create_order.py`: creates a catalog-backed sandbox order using real item-library variations and modifiers
- `scripts/create_payment.py`: creates a sandbox payment tied to the created order
- `scripts/list_catalog_items.py`: lists sellable catalog items and variation IDs
- `scripts/list_catalog_metadata.py`: lists catalog categories and modifier lists

## Requirements

- Python 3.12+ recommended
- a Square Sandbox access token
- `uv` recommended for environment management

## Setup

From the repository root:

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Create your local environment file from the example template:

```bash
cp .env.example .env
```

Then update `.env` with your real Square Sandbox access token:

```env
SQUARE_ACCESS_TOKEN=your_real_square_sandbox_access_token
```

## Run

Run the current loyalty account script from the repository root:

```bash
.venv/bin/python -m app.loyalty_list
```

The script prints:

- progress while records are fetched
- a formatted JSON list of the collected loyalty account records

Other useful commands:

```bash
.venv/bin/python -m app.loyalty_events
.venv/bin/python -m scripts.list_catalog_items
.venv/bin/python -m scripts.list_catalog_metadata
.venv/bin/python -m scripts.get_loyalty_program
.venv/bin/python -m scripts.create_customer
.venv/bin/python -m scripts.create_loyalty_account
.venv/bin/python -m scripts.create_order
.venv/bin/python -m scripts.create_payment
.venv/bin/python -m scripts.accumulate_loyalty_points
```

Use case split:

- `app/`: inspect or read data that already exists in the sandbox account
- `scripts/`: create the minimum controlled sandbox records needed for testing joins and API behavior

Example record shape:

```json
[
  {
    "loyalty_account_id": "abc123",
    "customer_id": "customer_001"
  }
]
```

## Proven Data Model

The current sandbox setup has already proven this end-to-end relationship:

```text
customer_id
J42RRWSJYDP85FKFD046MSRTV4
    ^
    |
loyalty_account_id
ad026a62-f825-4927-98a1-4e093bc9ea6f
    |
    v
loyalty_event_id
1c615539-ee49-3d34-8b82-2b5d896392db
    |
    v
order_id
t4uhAZfm9elAobsgz3aGguFsCPRZY
    |
    v
payment_id
jHRTyBi8lEMSHsjxZewUjwPiVEFZY
```

Interpretation:

- `customer_id` identifies the Square customer profile
- `loyalty_account_id` identifies that customer's loyalty membership
- `loyalty_event_id` identifies the points accrual event
- `order_id` identifies the catalog-backed purchase that triggered the loyalty event
- `payment_id` identifies the completed payment for that order

## Safety Notes

- Use `.env.example` as a public-safe template only. Do not put real secrets in it.
- Store real secrets only in your local `.env` file.
- `.env` is ignored by Git through `.gitignore` and should never be committed.
- Use Square Sandbox credentials for local development and public demo code.
- If a token is ever exposed, revoke it and create a new one.
- The script currently targets `SquareEnvironment.SANDBOX`
- Configuration fails fast if `SQUARE_ACCESS_TOKEN` is missing
- The current workflow is read-only

## Next Steps

Planned improvements:

- export results to CSV and JSON files
- add customers and orders data retrieval
- improve response validation and logging
- add lightweight tests
- document a more complete local development workflow
