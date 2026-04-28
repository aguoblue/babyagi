"""
Example 4: scope is also the function's global environment.

The function below uses SECRET and helper(), but neither is defined inside
the code string. We inject them into scope before exec runs.
"""

code_from_db = """
def greet(name):
    decorated_name = helper(name)
    return f"hello {decorated_name}, secret is {SECRET}"
"""

def helper(value):
    return value.upper()

scope = {
    "SECRET": "abc123",
    "helper": helper,
}

exec(code_from_db, scope)

greet = scope["greet"]

print(greet("tom"))
