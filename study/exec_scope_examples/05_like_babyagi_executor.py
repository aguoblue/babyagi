"""
Example 5: a tiny version of babyagi's executor idea.

Pretend this dictionary came from a database. The code field is just a string,
but exec can load it into scope as a real function.
"""

from pprint import pprint


function_version = {
    "name": "multiply",
    "code": """
def multiply(a, b):
    return a * b
""",
    "input_parameters": [
        {"name": "a", "type": "int"},
        {"name": "b", "type": "int"},
    ],
}

print("function_version from fake database:")
pprint(function_version)

local_scope = {}

exec(function_version["code"], local_scope)

function_name = function_version["name"]
func = local_scope[function_name]

print("loaded function object:", func)

output = func(6, 7)

print("output =", output)
