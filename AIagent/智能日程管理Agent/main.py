from agent import agent

def main():
    print("🤖 智能日程管理助手已启动！")
    print("输入命令开始交互（输入'退出'结束对话）")
    
    while True:
        user_input = input("\n你：")
        if user_input.lower() in ["退出", "bye", "exit"]:
            print("👋 再见！祝你有个高效的一天！")
            break
        if not user_input.strip():
            print("助手：请输入内容。")
            continue
        try:
            response = agent.invoke({"input": user_input})
            print(f"助手：{response.get('output', '无回复')}")
        except Exception as e:
            print(f"❌ 处理请求时出错：{str(e)}")

if __name__ == "__main__":
    main()