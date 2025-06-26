# 🚀 快速配置指南

## 第一步：设置API密钥

1. 打开 `config.py` 文件
2. 找到这一行：
   ```python
   DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your_deepseek_api_key_here")
   ```
3. 将 `"your_deepseek_api_key_here"` 替换为你的实际DeepSeek API密钥
4. 保存文件

## 第二步：安装依赖

### 方式一：使用安装脚本（推荐）

```bash
python install_deps.py
```

### 方式二：使用简化依赖文件

```bash
pip install -r requirements_simple.txt
```

### 方式三：手动安装核心依赖

```bash
pip install fastapi uvicorn pydantic python-dotenv requests openai streamlit
```

### 方式四：完整安装（如果上述方式失败）

```bash
# 先升级pip
python -m pip install --upgrade pip

# 逐个安装核心包
pip install fastapi
pip install uvicorn
pip install pydantic
pip install python-dotenv
pip install requests
pip install openai
pip install streamlit
```

## 第三步：检查配置

```bash
python check_config.py
```

## 第四步：启动系统

```bash
python start.py
```

## 第五步：访问系统

- 前端界面: http://localhost:8501
- 后端API: http://localhost:8000
- API文档: http://localhost:8000/docs

## 🔑 获取DeepSeek API密钥

1. 访问 [DeepSeek官网](https://platform.deepseek.com/)
2. 注册并登录账户
3. 进入API管理页面
4. 创建新的API密钥
5. 复制API密钥并粘贴到config.py文件中

## ❓ 常见问题

### Q: 安装依赖时出现编译错误
A: 尝试以下解决方案：
1. 使用 `python install_deps.py` 脚本
2. 或者使用 `pip install -r requirements_simple.txt`
3. 如果仍有问题，手动安装核心包

### Q: 启动时提示"配置检查失败"
A: 请确保已在config.py中正确设置了API密钥

### Q: 端口被占用
A: 修改config.py中的PORT设置，或关闭占用端口的程序

### Q: Python版本问题
A: 确保使用Python 3.8或更高版本

## 📞 技术支持

如果遇到问题，请：
1. 运行 `python check_config.py` 检查配置
2. 查看日志文件 `logs/app.log`
3. 运行测试脚本 `python test_system.py`
4. 查看详细使用指南 `USAGE.md` 