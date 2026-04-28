"""
Example 1: exec can run a Python code string.

This is the simplest form. The code string is executed immediately.
"""

code = """
print("hello from exec")
x = 10
y = 20
print("x + y =", x + y)
"""

exec(code)

print("After exec, x is available here:", x)
