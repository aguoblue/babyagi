"""A decorator can register functions into a dictionary."""

registry = {}


def register(name=None):
    def decorator(func):
        registered_name = name or func.__name__
        registry[registered_name] = func
        print(f"registered {registered_name!r}")
        return func

    return decorator


@register()
def world():
    return "world"


@register(name="hello")
def hello_world():
    return f"Hello {world()}!"


print("\nRegistry keys:", list(registry.keys()))
print("Direct call:", hello_world())
print("Registry call:", registry["hello"]())

