# exec and scope examples

Run these files one by one:

```bash
python study/exec_scope_examples/01_exec_plain_code.py
python study/exec_scope_examples/02_exec_with_scope.py
python study/exec_scope_examples/03_define_function_from_string.py
python study/exec_scope_examples/04_scope_as_function_environment.py
python study/exec_scope_examples/05_like_babyagi_executor.py
python study/exec_scope_examples/06_exec_code_with_import.py
python study/exec_scope_examples/07_function_depends_on_another_function.py
python study/exec_scope_examples/08_load_dependent_functions_in_steps.py
```

Core idea:

```python
scope = {}
exec("x = 1", scope)
print(scope["x"])
```

`exec` runs Python source code. The `scope` dictionary is where names created by that code are stored.
