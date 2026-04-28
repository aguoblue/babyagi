"""
04 - JSON API、状态码和错误处理。

运行:
    python3 study/flask_examples/04_json_api.py

试试:
    curl http://127.0.0.1:5000/api/books
    curl http://127.0.0.1:5000/api/books/1
    curl -X POST http://127.0.0.1:5000/api/books \
      -H "Content-Type: application/json" \
      -d '{"title": "Flask Web Development", "author": "Miguel Grinberg"}'
"""

from flask import Flask, abort, jsonify, request


app = Flask(__name__)


# 用内存列表模拟数据库。
# 程序重启后，新增的数据会消失。
BOOKS = [
    {"id": 1, "title": "The Pragmatic Programmer", "author": "Andrew Hunt"},
    {"id": 2, "title": "Clean Code", "author": "Robert C. Martin"},
]


@app.get("/")
def index():
    return jsonify(
        {
            "message": "JSON API 示例",
            "endpoints": ["/api/books", "/api/books/1"],
        }
    )


@app.get("/api/books")
def list_books():
    return jsonify({"items": BOOKS, "count": len(BOOKS)})


@app.get("/api/books/<int:book_id>")
def get_book(book_id):
    book = next((item for item in BOOKS if item["id"] == book_id), None)
    if book is None:
        # abort 会进入 Flask 错误处理流程。
        abort(404, description=f"Book {book_id} was not found")
    return jsonify(book)


@app.post("/api/books")
def create_book():
    # silent=True 表示 JSON 解析失败时返回 None，而不是直接抛异常。
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    author = data.get("author")

    if not title or not author:
        # 返回 (响应体, 状态码) 是 Flask 常用写法。
        return jsonify({"error": "title and author are required"}), 400

    book = {"id": len(BOOKS) + 1, "title": title, "author": author}
    BOOKS.append(book)
    return jsonify(book), 201


@app.errorhandler(404)
def not_found(error):
    # 统一把 404 变成 JSON。
    return jsonify({"error": "not_found", "message": error.description}), 404


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
