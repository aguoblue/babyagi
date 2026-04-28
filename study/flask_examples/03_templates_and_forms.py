"""
03 - 模板和表单。

运行:
    python3 study/flask_examples/03_templates_and_forms.py

打开:
    http://127.0.0.1:5000
"""

from flask import Flask, redirect, render_template_string, request, url_for


app = Flask(__name__)


@app.route("/")
def index():
    # render_template_string 会把字符串当成 Jinja2 模板渲染。
    # 真实项目通常会把模板放在 templates/*.html 文件里，然后用 render_template。
    todos = ["学习路由", "学习模板", "提交一个表单"]
    return render_template_string(
        """
        <!doctype html>
        <html lang="zh-CN">
          <head>
            <meta charset="utf-8">
            <title>模板示例</title>
          </head>
          <body>
            <h1>待办列表</h1>
            <ul>
              {% for todo in todos %}
                <li>{{ loop.index }}. {{ todo }}</li>
              {% endfor %}
            </ul>
            <p><a href="{{ url_for('contact') }}">去提交表单</a></p>
          </body>
        </html>
        """,
        todos=todos,
    )


@app.route("/contact", methods=["GET", "POST"])
def contact():
    # 同一个 URL 可以同时处理 GET 和 POST。
    # GET 用来展示表单，POST 用来处理提交。
    if request.method == "POST":
        name = request.form.get("name", "anonymous")
        message = request.form.get("message", "")
        return render_template_string(
            """
            <h1>表单提交成功</h1>
            <p>名字：{{ name }}</p>
            <p>留言：{{ message }}</p>
            <p><a href="{{ url_for('contact') }}">再提交一次</a></p>
            """,
            name=name,
            message=message,
        )

    return render_template_string(
        """
        <h1>Contact</h1>
        <form method="post">
          <p><input name="name" placeholder="你的名字"></p>
          <p><textarea name="message" placeholder="留言"></textarea></p>
          <p><button type="submit">提交</button></p>
        </form>
        <p><a href="{{ url_for('index') }}">返回首页</a></p>
        """
    )


@app.route("/go-home")
def go_home():
    # redirect 返回重定向响应。
    # 浏览器会再请求 url_for("index") 生成的地址。
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
