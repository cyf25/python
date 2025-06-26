# 校园生活服务智能助手使用指南

## 🚀 快速开始

### 1. 环境准备

确保你的系统已安装Python 3.8或更高版本：

```bash
python --version
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 配置API密钥

复制环境变量示例文件并配置你的DeepSeek API密钥：

```bash
# Windows
copy env_example.txt .env

# Linux/Mac
cp env_example.txt .env
```

编辑`.env`文件，添加你的DeepSeek API密钥：

```env
DEEPSEEK_API_KEY=your_actual_api_key_here
```

### 4. 启动系统

#### 方式一：使用启动脚本（推荐）

```bash
python start.py
```

#### 方式二：手动启动

**启动后端服务：**
```bash
python main.py
```

**启动前端界面：**
```bash
streamlit run frontend/app.py
```

### 5. 访问系统

- **前端界面**: http://localhost:8501
- **后端API**: http://localhost:8000
- **API文档**: http://localhost:8000/docs

## 📚 功能使用

### 智能问答

在聊天框中输入你的问题，AI助手会根据问题类型自动选择合适的服务：

- **课程相关**: "我想了解计算机科学课程"
- **导航相关**: "图书馆在哪里？"
- **生活服务**: "食堂的开放时间是什么？"
- **学习建议**: "我需要学习建议"

### 课程管理

#### 课程查询
- 询问具体课程信息
- 获取课程推荐
- 查看课程时间表

#### 学习计划
- 制定个性化学习计划
- 跟踪学习进度
- 获取学习建议

### 校园导航

#### 地点查询
- 查找教学楼、图书馆、食堂等
- 获取详细位置信息
- 查看开放时间

#### 路线规划
- 规划两点间路线
- 获取步行时间和距离
- 查看沿途地标

### 生活服务

#### 食堂信息
- 查询食堂位置和开放时间
- 了解餐饮选择
- 获取用餐建议

#### 其他服务
- 图书馆服务
- 医疗保健
- 银行ATM
- 便利店

### 心理健康支持

- 学习压力管理
- 情绪调节建议
- 专业资源推荐
- 危机干预指导

### 职业规划

- 职业方向分析
- 技能发展建议
- 实习就业指导
- 行业趋势分析

## 🎯 高级功能

### 用户资料设置

在侧边栏设置你的个人资料，获得更个性化的服务：

1. **专业**: 你的主修专业
2. **年级**: 当前年级
3. **兴趣**: 个人兴趣爱好
4. **已修学分**: 已获得的学分

### 快速操作

使用侧边栏的快速操作按钮：

- 📚 **课程推荐**: 基于你的资料推荐课程
- 🗺️ **校园导航**: 快速进入导航服务
- 🎓 **学习建议**: 获取学习指导
- 💬 **心理健康支持**: 寻求心理支持

### 对话管理

- **清空对话**: 清除当前对话历史
- **导出对话**: 下载对话记录为JSON文件
- **会话统计**: 查看对话统计信息

## 🔧 系统测试

运行测试脚本验证系统功能：

```bash
python test_system.py
```

测试包括：
- 健康检查
- 服务列表
- 聊天功能
- 课程推荐
- 导航功能
- 路线规划
- 学术问答
- 生活建议

## 📝 API使用

### 聊天接口

```bash
curl -X POST "http://localhost:8000/chat" \
  -H "Content-Type: application/json" \
  -d '{
    "message": "你好，我想了解计算机科学课程",
    "user_id": "user_001",
    "session_id": "session_123"
  }'
```

### 课程推荐

```bash
curl -X POST "http://localhost:8000/course/recommendations" \
  -H "Content-Type: application/json" \
  -d '{
    "user_profile": {
      "major": "计算机科学",
      "grade": "大二",
      "interests": ["编程", "人工智能"],
      "credits_earned": 30
    }
  }'
```

### 导航查询

```bash
curl -X POST "http://localhost:8000/navigation/find" \
  -H "Content-Type: application/json" \
  -d '{
    "location_name": "图书馆"
  }'
```

## 🛠️ 故障排除

### 常见问题

1. **API密钥错误**
   - 检查`.env`文件中的`DEEPSEEK_API_KEY`是否正确
   - 确认API密钥有效且有足够额度

2. **服务启动失败**
   - 检查端口是否被占用
   - 查看日志文件了解详细错误
   - 确保所有依赖已正确安装

3. **前端无法连接后端**
   - 确认后端服务正在运行
   - 检查API地址配置
   - 查看网络连接

4. **数据库错误**
   - 检查`data`目录权限
   - 删除数据库文件重新初始化
   - 查看数据库日志

### 日志查看

- **应用日志**: `logs/app.log`
- **系统日志**: 查看控制台输出

### 性能优化

- 调整`config.py`中的配置参数
- 优化数据库查询
- 使用缓存减少API调用

## 📞 技术支持

如果遇到问题，请：

1. 查看日志文件
2. 运行测试脚本
3. 检查配置是否正确
4. 参考API文档

## 🔄 更新维护

### 更新依赖

```bash
pip install -r requirements.txt --upgrade
```

### 备份数据

```bash
# 备份数据库
cp data/campus_assistant.db backup/campus_assistant_$(date +%Y%m%d).db

# 备份配置
cp .env backup/env_$(date +%Y%m%d).env
```

### 清理日志

```bash
# 清理旧日志
find logs/ -name "*.log" -mtime +7 -delete
``` 