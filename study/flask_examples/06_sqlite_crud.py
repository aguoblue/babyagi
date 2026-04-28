"""
06 - SQLite CRUD API。

这个示例只使用 Python 标准库 sqlite3，不额外引入 ORM。

运行:
    python3 study/flask_examples/06_sqlite_crud.py

试试:
    curl http://127.0.0.1:5000/tasks
    curl -X POST http://127.0.0.1:5000/tasks \
      -H "Content-Type: application/json" \
      -d '{"title": "learn flask sqlite"}'
    curl -X PATCH http://127.0.0.1:5000/tasks/1 \
      -H "Content-Type: application/json" \
      -d '{"done": true}'
"""

from pathlib import Path
import sqlite3

from flask import Flask, abort, g, jsonify, request


app = Flask(__name__)

# 数据库文件放在当前示例目录下。
DATABASE = Path(__file__).with_name("tasks.db")


def get_db():
    # g 是 Flask 的请求级临时存储。
    # 同一个请求里多次调用 get_db，只会创建一个连接。
    if "db" not in g:
        g.db = sqlite3.connect(DATABASE)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(error):
    # 请求结束后关闭数据库连接。
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    # IF NOT EXISTS 保证重复启动脚本时不会重复建表报错。
    db = get_db()
    db.execute(
        """
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            done INTEGER NOT NULL DEFAULT 0
        )
        """
    )
    db.commit()


def row_to_dict(row):
    # sqlite3.Row 可以像字典一样按列名读取，但 jsonify 更喜欢普通 dict。
    return {"id": row["id"], "title": row["title"], "done": bool(row["done"])}


@app.before_request
def ensure_db_exists():
    # 学习示例里为了简单，每个请求前确保表存在。
    # 真实项目通常会用迁移工具或启动脚本初始化数据库。
    init_db()


@app.get("/")
def index():
    return jsonify(
        {
            "message": "SQLite CRUD 示例",
            "endpoints": ["GET /tasks", "POST /tasks", "PATCH /tasks/<id>", "DELETE /tasks/<id>"],
        }
    )


@app.get("/tasks")
def list_tasks():
    rows = get_db().execute("SELECT * FROM tasks ORDER BY id DESC").fetchall()
    return jsonify({"items": [row_to_dict(row) for row in rows]})


@app.post("/tasks")
def create_task():
    data = request.get_json(silent=True) or {}
    title = data.get("title")
    if not title:
        return jsonify({"error": "title is required"}), 400

    cursor = get_db().execute("INSERT INTO tasks (title) VALUES (?)", (title,))
    get_db().commit()

    row = get_db().execute("SELECT * FROM tasks WHERE id = ?", (cursor.lastrowid,)).fetchone()
    return jsonify(row_to_dict(row)), 201


@app.patch("/tasks/<int:task_id>")
def update_task(task_id):
    data = request.get_json(silent=True) or {}
    allowed_fields = {}

    if "title" in data:
        allowed_fields["title"] = data["title"]
    if "done" in data:
        allowed_fields["done"] = 1 if data["done"] else 0

    if not allowed_fields:
        return jsonify({"error": "provide title or done"}), 400

    assignments = ", ".join(f"{field} = ?" for field in allowed_fields)
    values = list(allowed_fields.values()) + [task_id]
    get_db().execute(f"UPDATE tasks SET {assignments} WHERE id = ?", values)
    get_db().commit()

    row = get_db().execute("SELECT * FROM tasks WHERE id = ?", (task_id,)).fetchone()
    if row is None:
        abort(404, description=f"Task {task_id} was not found")
    return jsonify(row_to_dict(row))


@app.delete("/tasks/<int:task_id>")
def delete_task(task_id):
    cursor = get_db().execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    get_db().commit()
    if cursor.rowcount == 0:
        abort(404, description=f"Task {task_id} was not found")
    return "", 204


@app.errorhandler(404)
def not_found(error):
    return jsonify({"error": "not_found", "message": error.description}), 404


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
