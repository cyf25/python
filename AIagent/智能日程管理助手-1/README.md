# 智能日程管理助手

## 项目简介
智能日程管理助手是一个基于Vue.js的前端应用，旨在帮助用户管理日程、提醒和天气信息。该项目与后端服务相结合，提供了一个完整的智能助手体验。

## 功能
- **日历管理**：用户可以创建、查询和管理日程事件。
- **提醒功能**：用户可以设置和查看提醒事项。
- **天气查询**：用户可以查询指定城市的天气信息。

## 技术栈
- **前端**：Vue.js, Vite
- **后端**：Python, Flask (或其他后端框架)

## 项目结构
```
智能日程管理助手
├── backend
│   ├── agent.py
│   ├── config.py
│   ├── main.py
│   └── tools
│       ├── calendar.py
│       ├── reminder.py
│       └── weather.py
├── frontend
│   ├── public
│   │   └── index.html
│   ├── src
│   │   ├── App.vue
│   │   ├── main.js
│   │   ├── api
│   │   │   └── index.js
│   │   ├── components
│   │   │   ├── Calendar.vue
│   │   │   ├── Reminder.vue
│   │   │   └── Weather.vue
│   │   └── views
│   │       ├── Home.vue
│   │       └── About.vue
│   ├── package.json
│   └── vite.config.js
└── README.md
```

## 使用方法
1. 克隆项目到本地：
   ```
   git clone <repository-url>
   ```
2. 进入前端目录并安装依赖：
   ```
   cd frontend
   npm install
   ```
3. 启动开发服务器：
   ```
   npm run dev
   ```
4. 访问应用：
   打开浏览器并访问 `http://localhost:3000`。

## 贡献
欢迎任何形式的贡献！请提交问题或拉取请求。

## 许可证
本项目采用MIT许可证。