"""
Example 7: one exec-defined function can depend on another exec-defined function.

Both functions live in the same scope dictionary, so summarize() can find
normalize_name() when it is called.
"""

code_from_db = """
def normalize_name(name):
    return name.strip().title()

def summarize(user):
    name = normalize_name(user["name"])
    score = user["score"]
    return f"{name}: {score} points"
"""

scope = {}

exec(code_from_db, scope)

print("normalize_name in scope:", "normalize_name" in scope)
print("summarize in scope:", "summarize" in scope)

summarize = scope["summarize"]

print(summarize({"name": "  ada lovelace ", "score": 98}))
