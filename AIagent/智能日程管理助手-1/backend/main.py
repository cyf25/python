from agent import agent
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"msg": "Hello World"}

# 命令行交互主程序，只有直接运行 main.py 时才执行
def main():
    print("🤖 智能日程管理助手已启动！")
    print("输入命令开始交互（输入'退出'结束对话）")
    while True:
        user_input = input("\n你：")
        if user_input.lower() in ["退出", "bye", "exit"]:
            print("👋 再见！祝你有个高效的一天！")
            break
        try:
            response = agent.run(user_input)
            print(f"助手：{response}")
        except Exception as e:
            print(f"❌ 处理请求时出错：{str(e)}")

if __name__ == "__main__":
    main()