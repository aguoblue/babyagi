"""
02 - 路由参数、query 参数和 url_for。

运行:
    python3 study/flask_examples/02_routes_and_query.py

可访问:
    http://127.0.0.1:5000
    http://127.0.0.1:5000/users/Ada
    http://127.0.0.1:5000/posts/12
    http://127.0.0.1:5000/search?q=flask&page=2
"""

from flask import Flask, jsonify, request, url_for


app = Flask(__name__)


@app.route("/")
def index():
    # url_for 根据“视图函数名”生成 URL。
    # 比起手写 "/users/Ada"，url_for 更不容易在以后改路由时出错。
    links = {
        "user": url_for("user_profile", username="Ada"),
        "post": url_for("post_detail", post_id=12),
        "search": url_for("search", q="flask", page=2),
    }
    return jsonify(links)


@app.route("/users/<username>")
def user_profile(username):
    # <username> 会匹配路径中的一段字符串。
    # 访问 /users/Ada 时，username 的值就是 "Ada"。
    return f"用户主页: {username}"


@app.route("/posts/<int:post_id>")
def post_detail(post_id):
    # <int:post_id> 只匹配整数，并把参数转换成 int。
    # /posts/12 可以匹配，/posts/abc 不会匹配这个路由。
    return jsonify({"post_id": post_id, "type": type(post_id).__name__})


@app.route("/search")
def search():
    # request.args 读取 URL 问号后面的 query string。
    # /search?q=flask&page=2
    keyword = request.args.get("q", "")

    # type=int 会尝试把 page 转成整数。
    # 没传 page 时使用默认值 1。
    page = request.args.get("page", default=1, type=int)

    return jsonify({"keyword": keyword, "page": page})


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
