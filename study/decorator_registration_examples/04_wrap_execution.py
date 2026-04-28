"""A decorator can replace the original function with a wrapper."""

registry = {}


def execute(name, *args, **kwargs):
    print(f"[executor] loading {name!r} from registry")
    func = registry[name]
    result = func(*args, **kwargs)
    print(f"[executor] {name!r} returned {result!r}")
    return result


def register():
    def decorator(func):
        registry[func.__name__] = func
        print(f"registered {func.__name__!r}")


        def wrapper(*args, **kwargs):
            print("wrapper")
            return execute(func.__name__, *args, **kwargs)

        return wrapper

    return decorator


@register()
def add(a, b):
    return a + b


print("Calling add(2, 3):")
print(add(2, 3))

print("\nThe original implementation is stored in registry:")
print(registry["add"](10, 20))

