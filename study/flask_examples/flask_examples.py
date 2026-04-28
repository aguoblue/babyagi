"""
把常见 Flask 用法放在一个小应用里，方便边跑边看。

运行:
    python study/flask_examples.py

然后打开:
    http://127.0.0.1:5000

也可以用 curl 试试 JSON API:
    curl http://127.0.0.1:5000/api/books
    curl -X POST http://127.0.0.1:5000/api/books \
      -H "Content-Type: application/json" \
      -d '{"title": "Flask Web Development", "author": "Miguel Grinberg"}'
"""

from __future__ import annotations

from datetime import datetime, timezone
from time import perf_counter

from flask import (
    Flask,
    abort,  # 主动中断请求并返回指定错误码，比如 404。
    jsonify,  # 把 dict/list 转成 JSON 响应，并设置正确的 Content-Type。
    redirect,  # 返回重定向响应，让浏览器跳转到另一个地址。
    render_template_string,  # 直接从字符串渲染 Jinja2 模板，适合小示例。
    request,  # 当前请求对象，读取 query、form、json、headers 等。
    session,  # Flask 的签名 cookie 会话，适合存少量用户状态。
    url_for,  # 根据函数名反向生成 URL，避免把路径写死在页面里。
)


# Flask(__name__) 创建应用对象。
# __name__ 帮助 Flask 找到当前模块位置，进而定位模板、静态文件等资源。
app = Flask(__name__)

# session 需要 SECRET_KEY 对 cookie 签名。
# 这个值只适合本地学习；真实项目要放到环境变量里，并使用随机强密钥。
app.config["SECRET_KEY"] = "dev-only-secret-key"


# 这里用内存列表模拟数据库。
# 注意：每次重启程序数据都会恢复；真实项目通常会换成 SQLite/PostgreSQL 等数据库。
BOOKS = [
    {"id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin"},
]


@app.before_request
def start_timer() -> None:
    """在每个请求进入视图函数之前执行。"""
    # request 是“请求上下文”里的对象。
    # 在请求处理期间，给 request 挂一个临时属性，后面的 after_request 可以读到。
    request.start_time = perf_counter()


@app.after_request
def add_response_headers(response):
    """在每个响应返回给客户端之前执行。"""
    # 计算本次请求花了多少毫秒，并写到响应头里。
    # 访问任意接口后，可以在浏览器开发者工具或 curl -i 里看到 X-Elapsed-Ms。
    elapsed_ms = (perf_counter() - request.start_time) * 1000
    response.headers["X-Elapsed-Ms"] = f"{elapsed_ms:.2f}"

    # after_request 必须返回 response，否则 Flask 不知道最终要发什么。
    return response


@app.route("/")
def index():
    """首页：用模板渲染一段 HTML。"""
    # url_for("hello", name="Ada") 会根据 hello 函数对应的路由生成 /hello/Ada。
    # 这样以后改路由路径时，页面链接不容易漏改。
    routes = [
        ("Hello", url_for("hello", name="Ada")),
        ("Query params", url_for("search", q="flask", page=2)),
        ("JSON list API", url_for("list_books")),
        ("Path param API", url_for("get_book", book_id=1)),
        ("HTML form", url_for("contact")),
        ("Session counter", url_for("counter")),
        ("Redirect", url_for("old_home")),
        ("Custom 404", "/missing-page"),
    ]

    # render_template_string 会把字符串当成 Jinja2 模板。
    # {{ ... }} 表示输出变量，{% ... %} 表示控制语句，比如 for 循环。
    return render_template_string(
        """
        <!doctype html>
        <html lang="zh-CN">
          <head>
            <meta charset="utf-8">
            <title>Flask Examples</title>
            <style>
              body { font-family: system-ui, sans-serif; max-width: 760px; margin: 48px auto; line-height: 1.6; }
              code { background: #f4f4f5; padding: 2px 6px; border-radius: 4px; }
              li { margin: 8px 0; }
            </style>
          </head>
          <body>
            <h1>Flask 示例用法</h1>
            <p>这个页面由 <code>render_template_string</code> 渲染。</p>
            <ul>
              {% for label, href in routes %}
                <li><a href="{{ href }}">{{ label }}</a> - <code>{{ href }}</code></li>
              {% endfor %}
            </ul>
          </body>
        </html>
        """,
        routes=routes,
    )


@app.route("/hello")
@app.route("/hello/<name>")
def hello(name: str = "world"):
    """路由默认值和路径参数示例。"""
    # 同一个函数可以绑定多个路由。
    # 访问 /hello 时没有传 name，就使用函数默认值 world。
    # 访问 /hello/Ada 时，Flask 会把 Ada 作为 name 参数传进来。
    return f"Hello, {name}!"


@app.route("/search")
def search():
    """读取 query string 参数示例。"""
    # request.args 类似一个只读字典，对应 URL 问号后面的参数。
    # 例如 /search?q=flask&page=2 里，q 是 flask，page 是 2。
    keyword = request.args.get("q", "")

    # type=int 会尝试把参数转换成整数。
    # 如果没有 page，default=1 生效；如果无法转换，Flask 会返回 None。
    page = request.args.get("page", default=1, type=int)

    # jsonify 会把 Python 字典序列化成 JSON 响应。
    return jsonify(
        {
            "keyword": keyword,
            "page": page,
            "hint": "Try /search?q=python&page=3",
        }
    )


@app.get("/api/books")
def list_books():
    """GET 接口：返回图书列表。"""
    # @app.get(...) 是 @app.route(..., methods=["GET"]) 的简写。
    return jsonify({"items": BOOKS, "count": len(BOOKS)})


@app.get("/api/books/<int:book_id>")
def get_book(book_id: int):
    """GET 接口：读取单本书。"""
    # <int:book_id> 表示 Flask 只匹配整数路径，并把它转换成 int。
    # 例如 /api/books/1 可以匹配，/api/books/abc 不会匹配到这个函数。
    book = next((item for item in BOOKS if item["id"] == book_id), None)

    # abort 会抛出 HTTPException，交给 Flask 的错误处理流程。
    # 下面定义的 @app.errorhandler(404) 会统一处理这个 404。
    if book is None:
        abort(404, description=f"Book {book_id} was not found")
    return jsonify(book)


@app.post("/api/books")
def create_book():
    """POST 接口：接收 JSON 并创建一本书。"""
    # request.get_json() 用来读取 JSON 请求体。
    # silent=True 表示 JSON 格式不合法时不要直接报错，而是返回 None。
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    author = data.get("author")

    # Flask 允许返回 (body, status_code) 这样的元组。
    # 这里字段缺失时返回 400 Bad Request。
    if not title or not author:
        return jsonify({"error": "JSON fields 'title' and 'author' are required"}), 400

    # 这里只是学习示例，用 len(BOOKS) + 1 生成 id。
    # 多进程或真实数据库场景下，应该让数据库负责生成唯一 id。
    book = {"id": len(BOOKS) + 1, "title": title, "author": author}
    BOOKS.append(book)

    # 创建成功通常返回 201 Created。
    return jsonify(book), 201


@app.route("/contact", methods=["GET", "POST"])
def contact():
    """一个路由同时处理表单展示和表单提交。"""
    # 浏览器第一次打开 /contact 时是 GET，应该返回表单页面。
    # 用户点击提交后是 POST，应该读取表单内容并处理。
    if request.method == "POST":
        # request.form 读取 application/x-www-form-urlencoded 或 multipart/form-data 表单字段。
        name = request.form.get("name", "anonymous")
        message = request.form.get("message", "")

        # 模板默认会转义变量，能避免用户输入的 HTML 直接执行。
        return render_template_string(
            """
            <h1>收到表单</h1>
            <p><strong>{{ name }}</strong>: {{ message }}</p>
            <p><a href="{{ url_for('contact') }}">Back</a></p>
            """,
            name=name,
            message=message,
        )

    # GET 请求时返回一个最小 HTML 表单。
    # method="post" 表示提交时会用 POST 请求回到同一个 URL。
    return render_template_string(
        """
        <h1>Contact Form</h1>
        <form method="post">
          <p><input name="name" placeholder="Your name"></p>
          <p><textarea name="message" placeholder="Message"></textarea></p>
          <p><button type="submit">Send</button></p>
        </form>
        """
    )


@app.route("/counter")
def counter():
    """session 示例：记录当前浏览器访问次数。"""
    # Flask 默认把 session 存在客户端 cookie 里，但会用 SECRET_KEY 签名防篡改。
    # 它适合存少量、不敏感的数据；大量数据或敏感数据应放服务端存储。
    session["visits"] = session.get("visits", 0) + 1
    return jsonify({"visits": session["visits"]})


@app.route("/old-home")
def old_home():
    """重定向示例。"""
    # redirect(...) 返回 302 响应；浏览器收到后会再请求 Location 指向的新地址。
    return redirect(url_for("index"))


@app.route("/health")
def health():
    """健康检查接口示例。"""
    # 这类接口常用于部署平台、负载均衡或监控系统判断应用是否还活着。
    return jsonify(
        {
            "status": "ok",
            "utc_time": datetime.now(timezone.utc).isoformat(),
        }
    )


@app.errorhandler(404)
def not_found(error):
    """自定义 404 响应。"""
    # 所有没有匹配到路由的请求，以及 abort(404) 抛出的错误，都会走到这里。
    # API 项目里常返回 JSON；传统网站里也可以渲染一个 404.html 页面。
    return (
        jsonify(
            {
                "error": "not_found",
                "message": getattr(error, "description", "The page was not found"),
            }
        ),
        404,
    )


if __name__ == "__main__":
    # 只有直接运行这个文件时才会启动开发服务器。
    # 如果这个文件被其他模块 import，下面这行不会执行。
    #
    # debug=True 会开启调试模式和自动重载，适合本地学习。
    # 不要在生产环境打开 debug=True。
    app.run(debug=True, host="127.0.0.1", port=5000)
