# Flask 示例脚本

这个目录按“从简单到复杂”的顺序放了一组 Flask 学习脚本。每次只运行一个脚本即可。

如果当前 Python 环境没有 Flask，先安装依赖：

```bash
python3 -m pip install -r requirements.txt
```

## 推荐学习顺序

1. `01_hello.py`：最小 Flask 应用、基础路由、返回字符串。
2. `02_routes_and_query.py`：路径参数、类型转换、query 参数、`url_for`。
3. `03_templates_and_forms.py`：Jinja2 模板字符串、GET/POST 表单。
4. `04_json_api.py`：JSON API、状态码、简单参数校验、错误处理。
5. `05_blueprint_hooks_session.py`：Blueprint、请求钩子、响应头、session。
6. `06_sqlite_crud.py`：使用标准库 SQLite 做一个小型 CRUD API。

运行示例：

```bash
python3 study/flask_examples/01_hello.py
```

然后打开：

```text
http://127.0.0.1:5000
```

这些脚本都使用 `127.0.0.1:5000`。如果端口被占用，先停掉之前运行的脚本，或者修改脚本最后一行的 `port`。
