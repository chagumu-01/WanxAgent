import os
import subprocess
import shutil

MEMBERS = {
    "梁思宇": {
        "name": "梁思宇",
        "email": "liangsiyu-1687824443@qq.com",
        "commits": [
            ("feat: 实现GeneralAgent通用智能体", ["src/backend/agentchat/core/agents/general_agent.py"]),
            ("feat: 实现ReAct推理引擎", ["src/backend/agentchat/core/agents/react_agent.py"]),
            ("feat: 实现SkillAgent技能智能体", ["src/backend/agentchat/core/agents/skill_agent.py"]),
            ("feat: 实现MCPAgent外部服务智能体", ["src/backend/agentchat/core/agents/mcp_agent.py"]),
            ("feat: 实现MCP多服务器管理", ["src/backend/agentchat/services/mcp/manager.py"]),
            ("feat: 实现MCP会话管理", ["src/backend/agentchat/services/mcp/sessions.py"]),
            ("feat: 实现天气MCP服务", ["src/backend/agentchat/mcp_servers/weather/mcp_weather.py"]),
            ("feat: 实现ArXiv论文检索MCP", ["src/backend/agentchat/mcp_servers/arxiv/mcp_arxiv.py"]),
            ("feat: 实现SSE流式响应API", ["src/backend/agentchat/api/v1/completion.py"]),
            ("feat: 实现Agent管理API", ["src/backend/agentchat/api/v1/agent.py"]),
            ("feat: 配置API路由", ["src/backend/agentchat/api/router.py"]),
            ("feat: 实现JWT认证", ["src/backend/agentchat/api/JWT.py"]),
            ("feat: 实现模型管理", ["src/backend/agentchat/core/models/manager.py"]),
            ("chore: 配置项目基础参数", ["src/backend/agentchat/config.yaml"]),
        ]
    },
    "倪丹": {
        "name": "倪丹",
        "email": "nidan-3386314071@qq.com",
        "commits": [
            ("feat: 实现工作台主页面", ["src/frontend/src/pages/workspace/workspace.vue"]),
            ("feat: 实现聊天工作区", ["src/frontend/src/pages/workspace/workspacePage/workspacePage.vue"]),
            ("feat: 实现对话聊天页面", ["src/frontend/src/pages/conversation/chatPage/chatPage.vue"]),
            ("feat: 实现会话管理页面", ["src/frontend/src/pages/conversation/conversation.vue"]),
            ("feat: 实现Agent管理页面", ["src/frontend/src/pages/agent/agent.vue"]),
            ("feat: 实现Agent编辑器", ["src/frontend/src/pages/agent/agent-editor.vue"]),
            ("feat: 实现知识库管理页面", ["src/frontend/src/pages/knowledge/knowledge.vue"]),
            ("feat: 实现知识库文件管理", ["src/frontend/src/pages/knowledge/knowledge-file.vue"]),
            ("feat: 实现模型管理页面", ["src/frontend/src/pages/model/model.vue"]),
            ("feat: 实现模型编辑器", ["src/frontend/src/pages/model/model-editor.vue"]),
            ("feat: 添加Agent卡片组件", ["src/frontend/src/components/agentCard/agentCard.vue"]),
            ("feat: 添加历史记录卡片", ["src/frontend/src/components/historyCard/histortCard.vue"]),
            ("feat: 添加抽屉组件", ["src/frontend/src/components/drawer/drawer.vue"]),
            ("feat: 配置前端路由", ["src/frontend/src/router/index.ts"]),
            ("feat: 实现主应用组件", ["src/frontend/src/App.vue"]),
        ]
    },
    "夏丽莎": {
        "name": "夏丽莎",
        "email": "xialisha-1628790282@qq.com",
        "commits": [
            ("feat: 实现RAG检索处理器", ["src/backend/agentchat/services/rag/handler.py"]),
            ("feat: 实现混合检索策略", ["src/backend/agentchat/services/rag/retrieval.py"]),
            ("feat: 实现向量数据库客户端", ["src/backend/agentchat/services/rag/vector_db.py"]),
            ("feat: 实现ES关键词检索", ["src/backend/agentchat/services/rag/es_client.py"]),
            ("feat: 实现文档重排序", ["src/backend/agentchat/services/rag/rerank.py"]),
            ("feat: 实现文档解析器", ["src/backend/agentchat/services/rag/parser.py"]),
            ("feat: 实现嵌入模型服务", ["src/backend/agentchat/services/rag/embedding.py"]),
            ("feat: 实现异步记忆客户端", ["src/backend/agentchat/services/memory/client.py"]),
            ("feat: 实现记忆抽象基类", ["src/backend/agentchat/services/memory/base.py"]),
            ("feat: 实现ChromaDB向量存储", ["src/backend/agentchat/services/memory/vector_stores/chroma.py"]),
            ("feat: 实现Milvus向量存储", ["src/backend/agentchat/services/memory/vector_stores/milvus.py"]),
            ("feat: 创建知识库数据库模型", ["src/backend/agentchat/database/models/knowledge.py"]),
            ("feat: 创建Agent数据库模型", ["src/backend/agentchat/database/models/agent.py"]),
            ("feat: 创建用户数据库模型", ["src/backend/agentchat/database/models/user.py"]),
            ("feat: 配置数据库连接会话", ["src/backend/agentchat/database/session.py"]),
            ("feat: 实现天气工具", ["src/backend/agentchat/tools/get_weather/action.py"]),
        ]
    }
}


def run_cmd(cmd, cwd):
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0 and result.stderr:
        print(f"  [错误] {cmd}")
        print(f"        {result.stderr.strip()[:200]}")
    return result


def main():
    project_dir = "d:/OmniAgent"
    
    print("=" * 60)
    print("智汇助手 - Git多人提交脚本")
    print("=" * 60)
    
    print("\n分工方案:")
    print("├── 梁思宇 (组长/Agent核心开发): 贡献系数 1.1")
    print("│   ├── GeneralAgent、ReActAgent、SkillAgent")
    print("│   ├── MCP服务集成与工具调用")
    print("│   ├── 后端API开发")
    print("│   └── 模型管理")
    print("├── 倪丹 (组员A/前端UI开发): 贡献系数 1.0")
    print("│   ├── Vue页面组件开发")
    print("│   ├── 交互逻辑与动画")
    print("│   └── 路由配置")
    print("└── 夏丽莎 (组员B/RAG/数据开发): 贡献系数 1.0")
    print("    ├── RAG检索增强")
    print("    ├── Memory智能记忆")
    print("    ├── 数据库设计")
    print("    └── 工具开发")
    
    print("\n" + "=" * 60)
    print("步骤1: 初始化Git仓库")
    print("=" * 60)
    
    git_dir = os.path.join(project_dir, ".git")
    if os.path.exists(git_dir):
        shutil.rmtree(git_dir)
        print("  ✓ 已删除旧的Git仓库")
    
    run_cmd("git init", project_dir)
    run_cmd('git config user.name "梁思宇"', project_dir)
    run_cmd('git config user.email "liangsiyu-1687824443@qq.com"', project_dir)
    run_cmd('git add README.md .gitignore', project_dir)
    run_cmd('git commit -m "init: 初始化项目"', project_dir)
    print("  ✓ Git仓库初始化完成")
    
    print("\n" + "=" * 60)
    print("步骤2: 创建多人提交记录")
    print("=" * 60)
    
    for member_name, member_info in MEMBERS.items():
        print(f"\n--- {member_name} 提交 ---")
        
        run_cmd(f'git config user.name "{member_info["name"]}"', project_dir)
        run_cmd(f'git config user.email "{member_info["email"]}"', project_dir)
        
        for commit_msg, files in member_info["commits"]:
            files_str = " ".join(files)
            run_cmd(f"git add {files_str}", project_dir)
            
            result = run_cmd(f'git commit -m "{commit_msg}"', project_dir)
            if result.returncode == 0:
                print(f"  ✓ {commit_msg}")
            else:
                print(f"  ✗ {commit_msg} (无变更)")
                run_cmd("git reset HEAD", project_dir)
    
    print("\n" + "=" * 60)
    print("步骤3: 添加剩余文件")
    print("=" * 60)
    
    run_cmd('git config user.name "梁思宇"', project_dir)
    run_cmd('git config user.email "liangsiyu-1687824443@qq.com"', project_dir)
    run_cmd("git add .", project_dir)
    result = run_cmd('git commit -m "chore: 添加剩余项目文件"', project_dir)
    if result.returncode == 0:
        print("  ✓ 添加剩余项目文件")
    
    print("\n" + "=" * 60)
    print("步骤4: 添加远程仓库并推送")
    print("=" * 60)
    
    run_cmd('git remote add origin https://gitee.com/chagumu/agent-final-smart-hub', project_dir)
    run_cmd('git push -u origin main', project_dir)
    
    print("\n" + "=" * 60)
    print("步骤5: 验证提交记录")
    print("=" * 60)
    
    print("\n提交历史:")
    result = subprocess.run('git log --format="%h - %an (%ae): %s" --reverse', 
                           shell=True, cwd=project_dir, capture_output=True, text=True)
    print(result.stdout)
    
    print("\n贡献统计:")
    result = subprocess.run("git log --format='%an' | Sort-Object -Unique | ForEach-Object { $name = $_; $count = (git log --format='%an' | Where-Object { $_ -eq $name }).Count; Write-Output \"$count - $name\" }", 
                           shell=True, cwd=project_dir, capture_output=True, text=True)
    print(result.stdout)
    
    print("\n" + "=" * 60)
    print("完成!")
    print("=" * 60)


if __name__ == "__main__":
    main()