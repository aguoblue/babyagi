"""
Example 2: pass a scope dictionary to exec.

Names created by the code string are stored in that dictionary.
This is easier to inspect than letting exec write into the current file's globals.
"""

code = """
x = 10
y = 20
result = x + y
print(result)
"""

scope = {}

exec(code, scope)

print("scope keys:")
print(sorted(scope.keys()))

print("x =", scope["x"])
print("y =", scope["y"])
print("result =", scope["result"])
