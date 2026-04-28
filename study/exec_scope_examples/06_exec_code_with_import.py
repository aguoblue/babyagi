"""
Example 6: code loaded by exec can import modules.

The imported module name is stored in scope, just like variables and functions.
"""

code_from_db = """
import math

def circle_area(radius):
    return math.pi * radius * radius
"""

scope = {}

exec(code_from_db, scope)

print("math in scope:", "math" in scope)
print("circle_area in scope:", "circle_area" in scope)

circle_area = scope["circle_area"]

print("area =", circle_area(3))
