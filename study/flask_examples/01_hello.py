"""
01 - 最小 Flask 应用。

运行:
    python3 study/flask_examples/01_hello.py

打开:
    http://127.0.0.1:5000
"""

from flask import Flask


# 创建 Flask 应用对象。
# __name__ 表示当前模块名，Flask 用它定位当前文件所在目录。
app = Flask(__name__)


# @app.route("/") 把 URL 路径 "/" 绑定到下面的函数。
# 用户访问首页时，Flask 会调用 index()，并把返回值发给浏览器。
@app.route("/")
def index():
    return "Hello, Flask!"


@app.route("/about")
def about():
    return "这是一个最简单的 Flask 示例。"


if __name__ == "__main__":
    # debug=True 适合本地学习：代码变化后会自动重启，并显示详细错误页。
    # 生产环境不要开启 debug=True。
    app.run(debug=True, host="127.0.0.1", port=5000)
