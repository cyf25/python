# 校园生活服务智能助手

基于DeepSeek大模型的AI Agent校园生活服务智能助手，为学生提供全方位的校园生活支持。

## 功能特性

### 🎓 智能问答
- 校园政策咨询
- 学术问题解答
- 生活常识问答

### 📚 课程管理
- 课程查询和推荐
- 选课建议
- 学习计划制定

### 🗺️ 校园导航
- 地点查询
- 路线规划
- 校园地图服务

### 🎉 活动推荐
- 校园活动信息
- 社团活动推荐
- 学术讲座提醒

### 🍽️ 生活服务
- 食堂信息查询
- 图书馆服务
- 宿舍管理

### 📖 学习助手
- 学习计划制定
- 复习提醒
- 学习进度跟踪

## 技术架构

- **后端框架**: FastAPI
- **前端界面**: Streamlit
- **大模型**: DeepSeek
- **数据库**: SQLite
- **AI框架**: LangChain

## 🚀 快速开始

### 1. 配置API密钥

**重要**: 在 `config.py` 文件中直接设置你的DeepSeek API密钥：

```python
# 找到这一行并替换为你的实际API密钥
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY", "your_deepseek_api_key_here")
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动系统

```bash
python start.py
```

### 4. 访问系统

- **前端界面**: http://localhost:8501
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 📁 项目结构

```
campus_ai_assistant/
├── main.py                 # 主应用入口
├── config.py               # 配置文件（在这里设置API密钥）
├── start.py                # 启动脚本
├── agents/                 # AI Agent模块
├── services/               # 业务服务层
├── models/                 # 数据模型
├── frontend/               # 前端界面
└── data/                   # 数据文件
```

## 🔑 获取DeepSeek API密钥

1. 访问 [DeepSeek官网](https://platform.deepseek.com/)
2. 注册并登录账户
3. 进入API管理页面
4. 创建新的API密钥
5. 将API密钥粘贴到 `config.py` 文件中

## 使用说明

1. 启动系统后，访问 http://localhost:8501 使用Web界面
2. 在聊天框中输入你的问题或需求
3. AI助手会根据你的问题提供相应的服务和建议

## 开发计划

- [x] 基础框架搭建
- [x] AI Agent核心功能
- [x] 校园服务模块
- [ ] 移动端适配
- [ ] 多语言支持
- [ ] 语音交互功能

## 贡献指南

欢迎提交Issue和Pull Request来改进这个项目！

## 许可证

MIT License 