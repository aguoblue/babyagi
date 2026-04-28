"""The simplest decorator: @decorator is just function reassignment."""


def announce(func):
    print(f"decorating {func.__name__}")

    def wrapper():
        print("before call")
        result = func()
        print("after call")
        return result

    return wrapper


@announce
def say_hello():
    print("hello")


def say_world():
    print("world")


# This is exactly what @announce does behind the scenes.
say_world = announce(say_world)


print("\nCalling say_hello:")
say_hello()

print("\nCalling say_world:")
say_world()

