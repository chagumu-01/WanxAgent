<p align="center">
  <h1 align="center"> <img src="./imgs/logo.png" width="32" height="32" alt="WanxAgent Logo" /> WanxAgent </h1>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/vue-3.4+-4FC08D.svg?style=for-the-badge&logo=vue.js&logoColor=white" alt="Vue Version" />
  <img src="https://img.shields.io/badge/fastapi-0.115+-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge" alt="License" />
</p>

WanxAgent 是一个基于大语言模型的现代化智能对话系统，集成多Agent协作、知识库检索、工具调用、MCP服务器等核心能力，提供完整的AI工程解决方案。

## ✨ 核心特性

- **智能 Agent 协作**：支持多智能体协同工作，自动任务拆解与规划
- **增强型 RAG 系统**：全格式文档解析，混合检索与重排序优化
- **工具调用与 MCP 生态**：插件化工具扩展，原生支持 Model Context Protocol
- **多模型统一调度**：兼容主流大模型协议，支持流式响应与多轮对话
- **实时对话体验**：基于 SSE 的流式输出，响应式工作区设计
- **完善的权限体系**：JWT 安全认证，细粒度用户权限管理

## 展示图

### 首页

![产品总览](imgs/Home.png)

### 智能对话

![智能对话](imgs/Intelligent-Conversation.png)

### 知识库管理

![知识库管理](imgs/Knowledge-Base-Management.png)

### 工具与 MCP 服务

![工具与 MCP](imgs/Tool.png)

### 模型配置

![模型配置](imgs/Model.png)

### 数据看板

![数据看板](imgs/data.png)

## 🛠️ 技术栈

| 层级       | 技术                              |
| ---------- | --------------------------------- |
| 后端框架   | FastAPI + Uvicorn                 |
| AI 框架    | LangChain + LangGraph             |
| 数据库     | SQLite / MySQL                    |
| 缓存       | Redis / 本地缓存                  |
| 向量数据库 | ChromaDB                          |
| 前端框架   | Vue 3 + TypeScript + Element Plus |
| 构建工具   | Vite                              |

## 📁 项目结构

```
WanxAgent/
├── src/
│   ├── backend/
│   │   ├── agentchat/
│   │   │   ├── api/           # API 路由层
│   │   │   ├── core/          # 核心业务逻辑
│   │   │   ├── services/      # 服务层
│   │   │   ├── database/      # 数据访问层
│   │   │   ├── tools/         # 工具集
│   │   │   └── schema/        # 数据模型
│   │   └── requirements.txt
│   └── frontend/
│       ├── src/
│       │   ├── pages/         # 页面组件
│       │   ├── components/    # 通用组件
│       │   ├── api/           # API 调用
│       │   └── stores/        # 状态管理
│       └── package.json
├── docs/                      # 文档
├── imgs/                      # 截图资源
└── scripts/                   # 脚本工具
```

## 🚀 快速开始

### 环境要求

- Python 3.12+
- Node.js 18+

### 后端启动

```bash
cd src/backend
pip install -r requirements.txt
python -m uvicorn agentchat.main:app --port 7860
```

### 前端启动

```bash
cd src/frontend
npm install
npm run dev
```

## 🔧 配置说明

项目支持通过环境变量进行配置，主要配置项包括：

- `SERVER_HOST` / `SERVER_PORT`：服务地址和端口
- `MYSQL_ENDPOINT`：数据库连接地址（默认使用SQLite）
- `REDIS_ENDPOINT`：Redis连接地址（可选）
- `CONVERSATION_MODEL_API_KEY` / `CONVERSATION_MODEL_BASE_URL`：对话模型配置
- `STORAGE_MODE`：存储模式（local / minio）

## 📝 接口文档

启动后端服务后，访问 `http://localhost:7860/docs` 查看完整的 API 文档。

## 📊 功能模块

1. **用户认证模块**：登录、注册、JWT 鉴权
2. **对话管理模块**：创建对话、消息发送、历史记录
3. **Agent 管理模块**：Agent 创建、配置、技能绑定
4. **知识库模块**：文档上传、解析、检索
5. **工具管理模块**：工具注册、调用、MCP 集成
6. **模型管理模块**：多模型配置、路由调度

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！