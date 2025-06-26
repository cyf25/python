from flask import Flask, jsonify

# 初始化 Flask 应用
app = Flask(__name__)

# 定义 RESTful API 端点
@app.route('/hello', methods=['GET'])
def hello_world():
    try:
        # 返回 JSON 响应
        return jsonify({"message": "Hello, World!"})
    except Exception as e:
        # 错误处理
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    try:
        # 指定端口为 5001（避免与常见应用冲突）
        app.run(debug=True, port=5001)
    except Exception as e:
        print(f"启动失败: {e}")
        # 可以尝试其他端口
        app.run(debug=True, port=5002)