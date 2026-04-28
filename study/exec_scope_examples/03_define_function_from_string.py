"""
Example 3: define a function from a string, then call it.

After exec runs the code string, the function name appears in scope.
Then scope["add"] is a real Python function object.
"""

code_from_db = """
def add(a, b):
    return a + b
"""

scope = {}

exec(code_from_db, scope)

print("add in scope:", "add" in scope)
print("scope['add']:", scope["add"])

add_function = scope["add"]
result = add_function(2, 3)

print("result =", result)
