"""Why @register() has parentheses: it is a decorator factory."""


def tag(label):
    print(f"creating decorator with label={label!r}")

    def decorator(func):
        print(f"decorating {func.__name__}")
        func.label = label
        return func

    return decorator


@tag("important")
def task():
    return "done"


# The code above is equivalent to:
#
# def task():
#     return "done"
#
# task = tag("important")(task)


print(f"task result: {task()}")
print(f"task label: {task.label}")

