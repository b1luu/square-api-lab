from app.client import client

# Square exposes the seller's configured loyalty program under the special key "main".
result = client.loyalty.programs.get("main")

if result.errors:
    print(result.errors)
elif result.program is None:
    print("No loyalty program found.")
else:
    print(result.program.id)
