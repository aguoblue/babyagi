"""A tiny BabyAGI-style function registry with dependencies and execution logs."""

import inspect
from textwrap import dedent


class MiniFunctionSystem:
    def __init__(self):
        self.functions = {}

    def register_function(self, metadata=None, dependencies=None):
        metadata = metadata or {}
        dependencies = dependencies or []

        def decorator(func):
            source_lines = inspect.getsourcelines(func)[0]
            function_start = next(
                index for index, line in enumerate(source_lines)
                if line.strip().startswith("def ")
            )
            source = dedent("".join(source_lines[function_start:]))
            self.functions[func.__name__] = {
                "name": func.__name__,
                "source": source,
                "metadata": metadata,
                "dependencies": dependencies,
            }
            print(f"[register] {func.__name__}, dependencies={dependencies}")

            def wrapper(*args, **kwargs):
                return self.execute(func.__name__, *args, **kwargs)

            return wrapper

        return decorator

    def execute(self, name, *args, **kwargs):
        print(f"[execute] {name}")
        record = self.functions[name]

        local_scope = {}
        for dependency_name in record["dependencies"]:
            dependency_record = self.functions[dependency_name]
            exec(dependency_record["source"], local_scope)

        exec(record["source"], local_scope)
        func = local_scope[name]
        result = func(*args, **kwargs)
        print(f"[result] {name} -> {result!r}")
        return result


mini = MiniFunctionSystem()


@mini.register_function()
def world():
    return "world"


@mini.register_function(dependencies=["world"])
def hello_world():
    return f"Hello {world()}!"


print("\nRegistered function records:")
for function_name, record in mini.functions.items():
    print(f"- {function_name}: metadata={record['metadata']}, dependencies={record['dependencies']}")

print("\nCalling hello_world():")
hello_world()
