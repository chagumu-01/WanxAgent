<script setup lang="ts">
import { onMounted, ref, watch, computed } from "vue"
import { useRouter } from "vue-router"
import { useRoute } from "vue-router"
import { ElMessage, ElMessageBox } from 'element-plus'
import { User, FolderOpen, Compass, MessageSquare, Bot, Server, BookOpen, Puzzle, Wrench, Cpu, LayoutDashboard, LogOut } from 'lucide-vue-next'
import userAvatar from "../assets/user-avatar.svg"
import robotSvg from "../assets/robot.svg"
import agentchatSvg from "../assets/agentchat.svg"
import workspaceSvg from "../assets/workspace.svg"
import exploreSvg from "../assets/explore.svg"
import dialogSvg from "../assets/dialog.svg"
import mcpSvg from "../assets/mcp.svg"
import knowledgeSvg from "../assets/knowledge.svg"
import toolSvg from "../assets/tool.svg"
import skillSvg from "../assets/skill.svg"
import modelSvg from "../assets/model.svg"
import dashboardSvg from "../assets/dashboard.svg"
import { useAgentCardStore } from "../store/agent_card"
import { useUserStore } from "../store/user"
import { getAgentsAPI } from "../apis/agent"
import { logoutAPI, getUserInfoAPI } from "../apis/auth"
import { Agent } from "../type"

const agentCardStore = useAgentCardStore()
const userStore = useUserStore()
const route = useRoute()
const router = useRouter()
const itemName = ref("WanxAgent平台")
const showAppCenterMenu = ref(false)
let appCenterHoverTimer: any = null

const openAppCenterMenu = () => {
  if (appCenterHoverTimer) clearTimeout(appCenterHoverTimer)
  showAppCenterMenu.value = true
}

const closeAppCenterMenu = () => {
  if (appCenterHoverTimer) clearTimeout(appCenterHoverTimer)
  appCenterHoverTimer = setTimeout(() => {
    showAppCenterMenu.value = false
  }, 120)
}

const goWorkspaceTop = () => {
  router.push('/workspace')
}

const appCenterColumns = ref([
  [
    { label: '聊天', icon: MessageSquare, route: '/conversation' },
    { label: '任务', icon: FolderOpen, route: '/workspace' }
  ],
  [
    { label: '代理', icon: Bot, route: '/agent' },
    { label: '插件', icon: Puzzle, route: '/tool' }
  ],
  [
    { label: '知识', icon: BookOpen, route: '/knowledge' },
    { label: '模型', icon: Cpu, route: '/model' }
  ],
  [
    { label: '协议', icon: Server, route: '/mcp-server' },
    { label: '技能', icon: Wrench, route: '/agent-skill' }
  ]
])
const current = ref(route.meta.current)
const cardList = ref<Agent[]>([])

// 顶栏按钮激活态
const isWorkspaceActive = computed(() => route.path.startsWith('/workspace'))
const isAppCenterActive = computed(() => route.path.startsWith('/homepage'))

// 初始化用户状态
onMounted(async () => {
  userStore.initUserState()
  
  // 如果已登录但没有头像，则尝试获取用户信息
  if (userStore.isLoggedIn && userStore.userInfo && !userStore.userInfo.avatar) {
    try {
      const response = await getUserInfoAPI(userStore.userInfo.id)
      if (response.data.status_code === 200 && response.data.data) {
        const userData = response.data.data
        userStore.updateUserInfo({
          avatar: userData.user_avatar || userData.avatar || '/src/assets/user.svg',
          description: userData.user_description || userData.description
        })
      }
    } catch (error) {
      console.error('初始化时获取用户信息失败:', error)
    }
  }
  
  updateList()
})

const godefault = () => {
  agentCardStore.clear()
  router.push("/")
}
  
const updateList = async () => {
  try {
    const response = await getAgentsAPI()
    cardList.value = response.data.data
  } catch (error) {
    console.error('获取智能体列表失败:', error)
  }
}

const goCurrent = (item: string) => {
  const routes: Record<string, string> = {
    "homepage": "/homepage",
    "conversation": "/conversation",
    "agent": "/agent",
    "mcp-server": "/mcp-server",
    "knowledge": "/knowledge",
    "tool": "/tool",
    "agent-skill": "/agent-skill",
    "model": "/model",
    "workspace": "/workspace",
    "dashboard": "/dashboard"
  }
  
  router.push(routes[item] || "/")
}

// 用户下拉菜单命令处理
const handleUserCommand = async (command: string) => {
  switch (command) {
    case 'profile':
      router.push('/profile')
      break
    case 'settings':
      router.push('/configuration')
      break
    case 'logout':
      await handleLogout()
      break
  }
}

// 退出登录
const handleLogout = async () => {
  try {
    await logoutAPI()
  } catch (error) {
    console.error('调用登出接口失败:', error)
  }
  userStore.logout()
  ElMessage.success('已退出登录')
  router.push('/login')
}

// 头像加载错误处理
const handleAvatarError = (event: Event) => {
  const target = event.target as HTMLImageElement
  if (target) {
    target.src = '/src/assets/user.svg'
  }
}

watch(
  route,
  (val) => {
    current.value = route.meta.current
  },
  {
    immediate: true
  }
)
</script>

<template>
  <div class="ai-body">
    <div class="ai-nav">
      <div class="left">
        <div class="logo-section" @click="godefault">
          <img :src="robotSvg" class="logo-icon" />
          <img :src="agentchatSvg" class="brand-name" />
        </div>
      </div>
      <div class="right">
        <!-- 用户信息区域 -->
        <div class="user-info">
          <el-dropdown @command="handleUserCommand" trigger="click">
            <div class="user-avatar-wrapper">
              <div v-if="userStore.userInfo?.avatar" class="user-avatar">
                <img
                  :src="userStore.userInfo.avatar"
                  alt="用户头像"
                  @error="handleAvatarError"
                  referrerpolicy="no-referrer"
                />
              </div>
              <div v-else class="user-avatar-default">
                <img :src="userAvatar" class="user-icon-svg" />
              </div>
            </div>
            <template #dropdown>
              <el-dropdown-menu>
                <el-dropdown-item command="profile" :icon="User">
                  个人资料
                </el-dropdown-item>
                <el-dropdown-item divided command="logout">
                  <template #icon>
                    <LogOut :size="16" />
                  </template>
                  退出登录
                </el-dropdown-item>
              </el-dropdown-menu>
            </template>
          </el-dropdown>
        </div>
      </div>
    </div>
    <div class="ai-main">
      <el-col :span="2">
        <div class="sidebar-content">
          <el-menu
            class="el-menu-vertical-demo"
            :default-active="current"
          >
            <el-menu-item index="workspace" @click="goCurrent('workspace')">
              <template #title>
                <img :src="workspaceSvg" class="nav-icon" />
                <span>工作台</span>
              </template>
            </el-menu-item>
            <el-menu-item index="homepage" @click="goCurrent('homepage')">
              <template #title>
                <img :src="exploreSvg" class="nav-icon" />
                <span>探索</span>
              </template>
            </el-menu-item>
            <el-menu-item index="conversation" @click="goCurrent('conversation')">
              <template #title>
                <img :src="dialogSvg" class="nav-icon" />
                <span>会话</span>
              </template>
            </el-menu-item>
            <el-menu-item index="agent" @click="goCurrent('agent')">
              <template #title>
                <img :src="robotSvg" class="nav-icon" />
                <span>智能体</span>
              </template>
            </el-menu-item>
            <el-menu-item index="mcp-server" @click="goCurrent('mcp-server')">
              <template #title>
                <img :src="mcpSvg" class="nav-icon" />
                <span>MCP</span>
              </template>
            </el-menu-item>
            <el-menu-item index="knowledge" @click="goCurrent('knowledge')">
              <template #title>
                <img :src="knowledgeSvg" class="nav-icon" />
                <span>知识库</span>
              </template>
            </el-menu-item>
            <el-menu-item index="tool" @click="goCurrent('tool')">
              <template #title>
                <img :src="toolSvg" class="nav-icon" />
                <span>工具</span>
              </template>
            </el-menu-item>
            <el-menu-item index="agent-skill" @click="goCurrent('agent-skill')">
              <template #title>
                <img :src="skillSvg" class="nav-icon" />
                <span>Skill</span>
              </template>
            </el-menu-item>
            <el-menu-item index="model" @click="goCurrent('model')">
              <template #title>
                <img :src="modelSvg" class="nav-icon" />
                <span>模型</span>
              </template>
            </el-menu-item>
            <el-menu-item index="dashboard" @click="goCurrent('dashboard')">
              <template #title>
                <img :src="dashboardSvg" class="nav-icon" />
                <span>数据看板</span>
              </template>
            </el-menu-item>
          </el-menu>
        </div>
      </el-col>
      <div class="content">
        <router-view></router-view>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.ai-body {
  overflow: hidden;
  background-color: #F9F9F7;
  color: #111111;

  .ai-nav {
    display: flex;
    justify-content: space-between;
    align-items: center;
    height: 64px;
    background: #F9F9F7;
    padding: 0 24px;
    border-bottom: 1px solid #111111;
    position: relative;
    z-index: 3000;

    .left {
      display: flex;
      align-items: center;
      font-weight: 600;
      color: #111111;
      cursor: pointer;
      transition: all 0.2s ease-out;

      &:hover {
        opacity: 0.7;
      }

      .logo-section {
        display: flex;
        align-items: center;
        gap: 12px;
        cursor: pointer;

        .logo-icon {
          width: 36px;
          height: 36px;
          object-fit: contain;
          filter: grayscale(100%);
        }

        .brand-name {
          height: 36px;
          object-fit: contain;
          filter: grayscale(100%);
        }
      }
    }

    .right {
      display: flex;
      align-items: center;
      gap: 20px;

      .user-info {
        display: flex;
        align-items: center;
        gap: 12px;

        .user-avatar-wrapper {
          cursor: pointer;
          padding: 4px;
          background: transparent;
          border: 1px solid #111111;
          transition: all 0.2s ease-out;

          &:hover {
            background: #111111;
            box-shadow: 4px 4px 0px 0px #111111;
            transform: translate(-2px, -2px);
          }

          .user-avatar {
            img {
              width: 36px;
              height: 36px;
              object-fit: cover;
              border: 2px solid #111111;
              transition: all 0.2s ease-out;

              &:hover {
                border-color: #F9F9F7;
              }
            }
          }

          .user-avatar-default {
            width: 36px;
            height: 36px;
            border: 2px solid #111111;
            display: flex;
            align-items: center;
            justify-content: center;
            background: #111111;

            .user-icon-svg {
              width: 28px;
              height: 28px;
              filter: invert(100%);
            }
          }
        }
      }
    }
  }

  .ai-main {
    display: flex;
    height: calc(100vh - 64px);
    background-color: #F9F9F7;

    .sidebar-content {
      height: 100%;
      background-color: #F9F9F7;
      border-right: 1px solid #111111;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      transition: width 0.3s ease;

      .el-menu {
        border-right: none;
        background-color: #F9F9F7;
        color: #737373;

        .el-menu-item {
          height: 50px;
          line-height: 50px;
          font-size: 14px;
          font-weight: 500;
          color: #737373;
          text-transform: uppercase;
          letter-spacing: 0.05em;

          &.is-active {
            background-color: transparent !important;
            color: #CC0000 !important;
            border-right: 2px solid #CC0000;

            svg {
              color: #CC0000 !important;
            }
          }

          &:hover {
            background-color: #F5F5F5;
            color: #111111;

            svg {
              color: #111111;
            }
          }

          svg {
            margin-right: 10px;
            color: #737373;
            transition: color 0.2s ease-out;
          }

          .nav-icon {
            width: 20px;
            height: 20px;
            margin-right: 10px;
            filter: grayscale(100%) opacity(0.6);
            transition: all 0.2s ease-out;
          }

          &.is-active .nav-icon {
            filter: grayscale(100%) opacity(1);
          }

          &:hover .nav-icon {
            filter: grayscale(100%) opacity(1);
          }
        }
      }

      .sidebar-footer {
        padding: 16px;
        border-top: 1px solid #111111;

        .help-links {
          display: flex;
          justify-content: center;
          gap: 20px;

          .help-link {
            .help-icon {
              width: 24px;
              height: 24px;
              opacity: 0.4;
              transition: opacity 0.2s ease-out;
              filter: grayscale(100%);

              &:hover {
                opacity: 1;
              }
            }
          }
        }
      }
    }

    .content {
      flex: 1;
      padding: 24px;
      overflow-y: auto;
      background-color: #F9F9F7;
    }
  }
}
</style>
