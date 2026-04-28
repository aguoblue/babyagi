"""
Example 8: load dependent functions into the same scope in separate steps.

This is closer to a dynamic executor. The helper function is loaded first.
Later, another code string defines a function that calls that helper.
"""

helper_version = {
    "name": "format_price",
    "code": """
def format_price(cents):
    dollars = cents / 100
    return f"${dollars:.2f}"
""",
}

main_version = {
    "name": "receipt_line",
    "code": """
def receipt_line(item):
    price = format_price(item["price_cents"])
    return f'{item["name"]}: {price}'
""",
}

scope = {}

exec(helper_version["code"], scope)
exec(main_version["code"], scope)

format_price = scope["format_price"]
receipt_line = scope["receipt_line"]

print("helper output:", format_price(1299))
print("main output:", receipt_line({"name": "notebook", "price_cents": 1299}))
