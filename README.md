<p align="center">
  <h1 align="center"> <img src="./imgs/logo.png" width="32" height="32" alt="智汇助手 Logo" /> 智汇助手 </h1>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/python-3.12+-blue.svg?style=for-the-badge&logo=python&logoColor=white" alt="Python Version" />
  <img src="https://img.shields.io/badge/vue-3.4+-4FC08D.svg?style=for-the-badge&logo=vue.js&logoColor=white" alt="Vue Version" />
  <img src="https://img.shields.io/badge/fastapi-0.115+-009688.svg?style=for-the-badge&logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/license-MIT-green.svg?style=for-the-badge" alt="License" />
</p>

智汇助手是一款基于 AI Agent 的智能知识助手，集成 RAG 检索增强、MCP 外部服务连接、Skills 领域知识封装、Memory 智能记忆等高级功能，为用户提供精准、智能的问答服务。

## ✨ 核心特性

- **RAG 检索增强**：全格式文档解析，混合检索与重排序优化
- **MCP 外部连接**：插件化工具扩展，原生支持 Model Context Protocol
- **Skills 领域知识**：模块化技能封装，SKILL.md 文档驱动
- **Memory 智能记忆**：语义记忆、情景记忆、程序记忆三种类型
- **多工具协同**：Agent 自主编排多个工具完成多步任务
- **流式输出 + 动效**：基于 SSE 的流式响应，实时推送
- **完善的权限体系**：JWT 安全认证，细粒度用户权限管理

## 🎯 项目简介

### 做什么
智汇助手是一个全能型 AI Agent 平台，以 Agent 为核心驱动，具备明确的使用价值：
- 智能问答：基于知识库内容进行精准回答
- 任务执行：自主编排工具完成复杂任务
- 知识管理：文档上传、解析、检索一体化

### 解决什么问题
- 传统问答系统无法理解上下文和用户偏好
- 单一工具无法完成复杂的多步任务
- 知识分散，难以统一管理和检索

## 📊 功能模块

1. **用户认证模块**：登录、注册、JWT 鉴权
2. **对话管理模块**：创建对话、消息发送、历史记录
3. **Agent 管理模块**：Agent 创建、配置、技能绑定
4. **知识库模块**：文档上传、解析、检索（RAG）
5. **工具管理模块**：工具注册、调用、MCP 集成
6. **模型管理模块**：多模型配置、路由调度

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

## 🛠️ 技术选型

| 层级 | 技术 | 选型理由 |
|------|------|---------|
| 后端框架 | FastAPI + Uvicorn | 高性能、异步支持、自动 API 文档 |
| AI 框架 | LangChain + LangGraph | 强大的 Agent 编排能力、工具集成 |
| 数据库 | SQLite / MySQL | SQLite 适合开发测试，MySQL 适合生产环境 |
| 缓存 | Redis / 本地缓存 | 分布式缓存 + 本地缓存降级方案 |
| 向量数据库 | ChromaDB / Milvus | ChromaDB 零运维适合开发，Milvus 高性能适合生产 |
| 前端框架 | Vue 3 + TypeScript + Element Plus | 响应式设计、类型安全、组件丰富 |
| 构建工具 | Vite | 快速开发体验、按需加载 |
| 模型服务 | DeepSeek / Zhipu GLM | 低成本、高性能、API 兼容 |

## 📁 项目结构

```
智汇助手/
├── src/
│   ├── backend/
│   │   ├── agentchat/
│   │   │   ├── api/           # API 路由层
│   │   │   ├── core/          # 核心业务逻辑（Agent实现）
│   │   │   ├── services/      # 服务层（RAG/MCP/Memory）
│   │   │   ├── database/      # 数据访问层
│   │   │   ├── tools/         # 工具集
│   │   │   ├── mcp_servers/   # MCP服务器示例
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
- Node.js 18+ / Bun 1.0+

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

或者使用 Bun：

```bash
cd src/frontend
bun install
bun dev
```

### 访问地址

- 前端页面：http://localhost:8090
- 后端 API：http://localhost:7860
- API 文档：http://localhost:7860/docs

## 🔧 环境变量配置

### 后端配置

创建 `.env` 文件或修改 `src/backend/agentchat/config.yaml`：

```yaml
# 服务器配置
server:
  host: 0.0.0.0
  port: 7860

# 数据库配置（默认SQLite，可切换MySQL）
database:
  type: sqlite
  sqlite_path: agentchat.sqlite
  # mysql_url: mysql://user:password@localhost:3306/agentchat

# 缓存配置（默认本地缓存，可切换Redis）
cache:
  type: local
  # redis_url: redis://localhost:6379/0

# AI模型配置
models:
  conversation:
    api_key: ""
    base_url: "https://api.deepseek.com"
    model_name: "deepseek-chat"
  embedding:
    api_key: ""
    base_url: "https://api.deepseek.com"
    model_name: "text-embedding-3-large"

# RAG配置
rag:
  vector_db:
    mode: "chroma"  # chroma 或 milvus

# 存储配置
storage:
  mode: local
```

### 前端配置

修改 `src/frontend/.env`：

```bash
VITE_API_BASE_URL=http://localhost:7860
```

## 📦 目录结构说明

### 后端目录

| 目录 | 说明 |
|------|------|
| `api/` | RESTful API 路由和控制器 |
| `core/agents/` | Agent 核心实现（GeneralAgent、ReActAgent、SkillAgent等） |
| `services/rag/` | RAG 检索增强服务（文档解析、向量检索、重排序） |
| `services/mcp/` | MCP 外部服务连接（多服务器管理、工具调用） |
| `services/memory/` | Memory 智能记忆服务（语义/情景/程序记忆） |
| `tools/` | 自定义工具集（天气、搜索、文件转换等） |
| `mcp_servers/` | MCP 服务器示例（飞书日历、天气、ArXiv） |
| `database/` | 数据库模型和数据访问层 |

### 前端目录

| 目录 | 说明 |
|------|------|
| `pages/` | 页面组件（工作台、对话、知识库、工具、模型等） |
| `components/` | 通用组件（Agent卡片、历史记录卡片、弹窗等） |
| `api/` | API 调用封装 |
| `assets/` | 静态资源（图标、图片） |

## 👥 分工说明

### 组员信息

| 姓名 | QQ号 | 角色 | 贡献系数 |
|------|------|------|---------|
| 梁思宇 | 1687824443 | Agent 核心开发（组长） | 1.1 |
| 倪丹 | 3386314071 | 前端 UI 开发 | 1.0 |
| 夏丽莎 | 1628790282 | RAG / 数据开发 | 1.0 |

### 职责分配

**梁斯禹（Agent 核心开发 / 组长）**
- Agent 架构设计与实现（GeneralAgent、ReActAgent、SkillAgent、MCPAgent）
- MCP 服务集成与工具调用（天气、ArXiv、飞书日历）
- Skills 领域知识封装
- 后端 API 开发与调试（JWT认证、流式响应）
- 模型管理与配置

**倪聃（前端 UI 开发）**
- Vue 3 页面组件开发（工作台、对话、Agent管理、知识库、模型管理）
- 交互逻辑与动画效果
- 响应式布局设计
- 流式输出动效实现
- 前端路由配置

**夏莉莎（RAG / 数据开发）**
- 文档解析与索引构建（PDF/Word/PPT/Markdown）
- 向量检索与重排序优化（ES + ChromaDB）
- Memory 智能记忆系统（语义/情景/程序记忆）
- 数据库设计与实现
- 工具开发（天气、网页搜索）

### 贡献说明

项目采用 Git 多人协作开发，每位组员都有独立的 commit 记录，体现个人贡献。组长负责核心模块开发，工作量相对较多；两位组员分别负责前端和数据模块，工作量相当。贡献系数根据实际工作量分配，符合公平性原则。

## 📝 接口文档

启动后端服务后，访问 `http://localhost:7860/docs` 查看完整的 API 文档。

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

**项目名称**：智汇助手  
**课程**：AI Agent 应用开发实战  
**小组**：3人小组  
**提交日期**：2026年夏季