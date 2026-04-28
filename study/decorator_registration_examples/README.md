# Decorator registration examples

These examples explain the `@register_function()` style used by BabyAGI.

Run them one by one:

```bash
python study/decorator_registration_examples/01_decorator_basics.py
python study/decorator_registration_examples/02_decorator_with_parentheses.py
python study/decorator_registration_examples/03_register_into_dict.py
python study/decorator_registration_examples/04_wrap_execution.py
python study/decorator_registration_examples/05_mini_babyagi_style.py
```

## Learning path

- `01_decorator_basics.py`: `@decorator` is just assignment after function creation.
- `02_decorator_with_parentheses.py`: `@factory(...)` first creates a decorator.
- `03_register_into_dict.py`: a decorator can register functions into a table.
- `04_wrap_execution.py`: a decorator can replace a function with a wrapper.
- `05_mini_babyagi_style.py`: registration plus dependencies plus executor, like a tiny BabyAGI.

