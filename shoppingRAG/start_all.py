import subprocess
import os
import time

# 启动 FastAPI 后端
backend_cmd = ["uvicorn", "app:app", "--reload"]
subprocess.Popen(["cmd", "/k"] + backend_cmd, creationflags=subprocess.CREATE_NEW_CONSOLE)

# 等待后端启动片刻
time.sleep(2)

# 启动 React 前端
frontend_dir = os.path.join(os.getcwd(), "chat-frontend")
frontend_cmd = ["npm", "start"]
subprocess.Popen(["cmd", "/k"] + frontend_cmd, cwd=frontend_dir, creationflags=subprocess.CREATE_NEW_CONSOLE)

print("所有服务已启动，请在浏览器访问 http://localhost:3000")
input("按回车键退出本窗口（服务不受影响）...") 