"""
05 - Blueprint、请求钩子和 session。

运行:
    python3 study/flask_examples/05_blueprint_hooks_session.py

可访问:
    http://127.0.0.1:5000
    http://127.0.0.1:5000/api/ping
    http://127.0.0.1:5000/visits
"""

from time import perf_counter

from flask import Blueprint, Flask, jsonify, request, session


app = Flask(__name__)

# session 依赖 SECRET_KEY 做签名。
# 真实项目不要把密钥写死在代码里。
app.config["SECRET_KEY"] = "dev-only-secret-key"


# Blueprint 可以把一组相关路由组织在一起。
# 项目变大后，通常会按业务拆成多个 blueprint。
api = Blueprint("api", __name__, url_prefix="/api")


@app.before_request
def before_request():
    # 请求进入任何视图函数前都会执行。
    request.start_time = perf_counter()


@app.after_request
def after_request(response):
    # 视图函数返回响应后，真正发给浏览器前执行。
    elapsed_ms = (perf_counter() - request.start_time) * 1000
    response.headers["X-Elapsed-Ms"] = f"{elapsed_ms:.2f}"
    return response


@app.route("/")
def index():
    return "访问 /api/ping 看 Blueprint；访问 /visits 看 session。"


@app.route("/visits")
def visits():
    # Flask 默认 session 存在客户端 cookie 里，并用 SECRET_KEY 防篡改。
    session["visits"] = session.get("visits", 0) + 1
    return jsonify({"visits": session["visits"]})


@api.get("/ping")
def ping():
    # 因为 blueprint 设置了 url_prefix="/api"，所以完整路径是 /api/ping。
    return jsonify({"message": "pong"})


# 注册 blueprint 之后，里面定义的路由才会挂到 app 上。
app.register_blueprint(api)


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
