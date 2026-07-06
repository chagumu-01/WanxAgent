<script setup lang="ts">
import { ref, onMounted, computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { 
  User, 
  Home, 
  MessageSquare, 
  Bot, 
  Puzzle, 
  BookOpen, 
  Cpu, 
  Server,
  FolderOpen,
  Plus,
  Trash2,
  ChevronRight,
  LogOut
} from 'lucide-vue-next'
import robotSvg from '../../assets/robot.svg'
import agentchatSvg from '../../assets/agentchat.svg'
import { useUserStore } from '../../store/user'
import { logoutAPI, getUserInfoAPI } from '../../apis/auth'
import { fallbackToDefaultUserAvatar, getUserAvatarSrc } from '../../utils/avatar'
import { 
  getWorkspaceSessionsAPI, 
  deleteWorkspaceSessionAPI 
} from '../../apis/workspace'

const router = useRouter()
import { useRoute } from 'vue-router'
const route = useRoute()
const userStore = useUserStore()
const selectedSession = ref('')
const sessions = ref<any[]>([])
const loading = ref(false)

const formatTime = (timeStr: string) => {
  try {
    if (!timeStr) return '未知时间'
    
    const date = new Date(timeStr)
    if (isNaN(date.getTime())) {
      return '未知时间'
    }
    
    const now = new Date()
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60)
    
    if (diffInHours < 1) return '刚刚'
    if (diffInHours < 24) return `${Math.floor(diffInHours)}小时前`
    if (diffInHours < 24 * 7) return `${Math.floor(diffInHours / 24)}天前`
    return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
  } catch (error) {
    return '未知时间'
  }
}

const fetchSessions = async () => {
  try {
    loading.value = true
    const response = await getWorkspaceSessionsAPI()
    if (response.data.status_code === 200) {
      sessions.value = response.data.data.map((session: any) => ({
        sessionId: session.session_id || session.id,
        title: session.title || '未命名会话',
        createTime: session.create_time || session.created_at || new Date().toISOString(),
        agent: session.agent || 'lingseek',
        contexts: session.contexts || []
      }))
      console.log('工作区会话列表:', sessions.value)
    } else {
      ElMessage.error('获取会话列表失败')
    }
  } catch (error) {
    console.error('获取会话列表出错:', error)
    ElMessage.error('获取会话列表失败')
  } finally {
    loading.value = false
  }
}

const deleteSession = async (sessionId: string, event: Event) => {
  event.stopPropagation()
  
  try {
    const response = await deleteWorkspaceSessionAPI(sessionId)
    if (response.data.status_code === 200) {
      ElMessage.success('会话删除成功')
      await fetchSessions()
      
      if (selectedSession.value === sessionId) {
        selectedSession.value = ''
        router.push('/workspace')
      }
    } else {
      ElMessage.error('删除会话失败')
    }
  } catch (error) {
    console.error('删除会话出错:', error)
    ElMessage.error('删除会话失败')
  }
}

const selectSession = (sessionId: string) => {
  selectedSession.value = sessionId
  
  const session = sessions.value.find(s => s.sessionId === sessionId)
  
  if (!session) {
    console.error('未找到会话:', sessionId)
    return
  }
  
  console.log('选择会话:', sessionId, '类型:', session.agent)
  
  if (session.agent === 'simple') {
    router.push({
      name: 'workspaceDefaultPage',
      query: {
        session_id: sessionId
      }
    })
  } else {
    router.push({
      name: 'taskGraphPage',
      query: {
        session_id: sessionId
      }
    })
  }
}

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

const handleAvatarError = (event: Event) => {
  fallbackToDefaultUserAvatar(event)
}

const goToHomepage = () => {
  router.push('/homepage')
}

const goToWorkspace = () => {
  router.push('/workspace')
}

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

const appCenterColumns = ref([
  [
    { label: '会话', icon: MessageSquare, route: '/conversation' },
    { label: '工作台', icon: FolderOpen, route: '/workspace' }
  ],
  [
    { label: '智能体', icon: Bot, route: '/agent' },
    { label: '工具', icon: Puzzle, route: '/tool' }
  ],
  [
    { label: '知识库', icon: BookOpen, route: '/knowledge' },
    { label: '模型', icon: Cpu, route: '/model' }
  ],
  [
    { label: 'MCP', icon: Server, route: '/mcp-server' }
  ]
])

const isWorkspaceActive = computed(() => route.path.startsWith('/workspace'))
const isAppCenterActive = computed(() => route.path.startsWith('/homepage'))

onMounted(async () => {
  userStore.initUserState()
  
  if (userStore.isLoggedIn && userStore.userInfo && !userStore.userInfo.avatar) {
    try {
      const response = await getUserInfoAPI(userStore.userInfo.id)
      if (response.data.status_code === 200 && response.data.data) {
        const userData = response.data.data
        userStore.updateUserInfo({
          avatar: userData.user_avatar || userData.avatar || '',
          description: userData.user_description || userData.description
        })
      }
    } catch (error) {
      console.error('初始化时获取用户信息失败:', error)
    }
  }
  
  await fetchSessions()
})
</script>

<template>
  <div class="workspace-container">
    <div class="workspace-nav">
      <div class="nav-left">
        <div class="logo-section">
          <img :src="robotSvg" class="logo-icon" />
          <img :src="agentchatSvg" class="brand-name" />
        </div>
      </div>
      <div class="nav-right">
        <div class="nav-links">
          <button 
            @click="goToHomepage" 
            :class="['nav-link', { active: isAppCenterActive }]"
          >
            <Home :size="18" />
            <span>应用中心</span>
          </button>
          <button 
            @click="goToWorkspace" 
            :class="['nav-link', { active: isWorkspaceActive }]"
          >
            <FolderOpen :size="18" />
            <span>工作台</span>
          </button>
        </div>
        <div class="user-info">
          <el-dropdown @command="handleUserCommand" trigger="click">
            <div class="user-avatar-wrapper">
              <div class="user-avatar">
                <img
                  :src="getUserAvatarSrc(userStore.userInfo?.avatar)"
                  alt="用户头像"
                  @error="handleAvatarError"
                  referrerpolicy="no-referrer"
                />
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

    <div class="workspace-main">
    <div class="sidebar">
      <div class="create-section">
        <button @click="goToHomepage" class="create-btn-native">
          <div class="btn-content">
            <Plus :size="24" />
            <span>新建会话</span>
          </div>
        </button>
      </div>

      <div class="session-list">
        <div v-if="loading" class="loading-state">
          <div class="loading-icon">⏳</div>
          <div class="loading-text">正在加载会话列表...</div>
        </div>

        <div v-else-if="sessions.length === 0" class="empty-state">
          <div class="empty-icon">
            <MessageSquare :size="48" />
          </div>
          <div class="empty-text">暂无会话记录</div>
        </div>

        <div
          v-for="session in sessions"
          :key="session.sessionId"
          :class="['session-card', { active: selectedSession === session.sessionId }]"
          @click="selectSession(session.sessionId)"
        >
          <div class="session-icon">
            <FolderOpen :size="22" />
          </div>
          <div class="session-info">
            <div class="session-title">{{ session.title }}</div>
            <div class="session-time">{{ formatTime(session.createTime) }}</div>
          </div>
          <button
            class="delete-btn"
            @click="deleteSession(session.sessionId, $event)"
            title="删除会话"
          >
            <Trash2 :size="16" />
          </button>
        </div>
      </div>
    </div>

    <div class="content">
      <router-view />
    </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.workspace-container {
  width: 100%;
  height: 100vh;
  display: flex;
  flex-direction: column;
  background-color: #fceef2;
}

.workspace-nav {
  display: flex;
  justify-content: space-between;
  align-items: center;
  height: 64px;
  background: #ffffff;
  padding: 0 24px;
  box-shadow: 0 1px 4px rgba(196, 30, 58, 0.1);
  position: relative;
  z-index: 3000;

  .nav-left {
    display: flex;
    align-items: center;

    .logo-section {
      display: flex;
      align-items: center;
      gap: 12px;

      .logo-icon {
        width: 36px;
        height: 36px;
        object-fit: contain;
      }

      .brand-name {
        height: 36px;
        object-fit: contain;
      }
    }
  }

  .nav-right {
    display: flex;
    align-items: center;
    gap: 20px;

    .nav-links {
      display: flex;
      gap: 8px;

      .nav-link {
        display: flex;
        align-items: center;
        gap: 6px;
        padding: 8px 16px;
        border-radius: 8px;
        font-size: 14px;
        font-weight: 500;
        color: #c41e3a;
        background: transparent;
        border: 1px solid transparent;
        cursor: pointer;
        transition: all 0.2s ease;

        &:hover {
          background: rgba(196, 30, 58, 0.08);
          border-color: rgba(196, 30, 58, 0.2);
        }

        &.active {
          background: linear-gradient(135deg, rgba(196, 30, 58, 0.1), rgba(217, 69, 96, 0.1));
          border-color: #c41e3a;
          color: #c41e3a;
        }
      }
    }

    .user-info {
      .user-avatar-wrapper {
        display: flex;
        align-items: center;
        padding: 4px;
        border-radius: 50%;
        background: rgba(196, 30, 58, 0.1);
        backdrop-filter: blur(10px);
        cursor: pointer;
        transition: all 0.3s ease;
        border: 1px solid rgba(196, 30, 58, 0.2);

        &:hover {
          background: rgba(196, 30, 58, 0.2);
          transform: translateY(-2px);
          box-shadow: 0 8px 16px rgba(196, 30, 58, 0.15);
          border-color: #c41e3a;
        }

        .user-avatar {
          img {
            width: 36px;
            height: 36px;
            border-radius: 50%;
            border: 2px solid #c41e3a;
            object-fit: cover;
            box-shadow: 0 4px 10px rgba(196, 30, 58, 0.2);
            transition: all 0.3s ease;

            &:hover {
              border-color: #9e1830;
              transform: scale(1.05);
            }
          }
        }

        .user-avatar-default {
          width: 36px;
          height: 36px;
          border-radius: 50%;
          border: 2px solid #c41e3a;
          display: flex;
          align-items: center;
          justify-content: center;
          background: #c41e3a;
          box-shadow: 0 4px 10px rgba(196, 30, 58, 0.2);

          .user-icon-svg {
            width: 28px;
            height: 28px;
          }
        }
      }
    }
  }
}

.workspace-main {
  display: flex;
  flex: 1;
  height: calc(100vh - 64px);
  background-color: #fceef2;

  .sidebar {
    height: 100%;
    width: 280px;
    background-color: #ffffff;
    border-right: 1px solid #f2a5b5;
    display: flex;
    flex-direction: column;
    box-shadow: 2px 0 8px rgba(196, 30, 58, 0.05);

    .create-section {
      padding: 20px 16px;

      .create-btn-native {
        width: 100%;
        height: 48px;
        border-radius: 12px;
        font-weight: 600;
        transition: all 0.3s ease;
        background: linear-gradient(135deg, #c41e3a, #d94560);
        color: white;
        border: none;
        cursor: pointer;
        font-size: 15px;
        letter-spacing: 1px;
        box-shadow: 0 4px 12px rgba(196, 30, 58, 0.3);

        &:hover {
          transform: translateY(-1px);
          box-shadow: 0 6px 16px rgba(196, 30, 58, 0.4);
        }

        &:active {
          transform: translateY(0);
        }

        .btn-content {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;
        }
      }
    }

    .session-list {
      flex: 1;
      padding: 8px;
      overflow-y: auto;

      .loading-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 200px;
        color: #c41e3a;

        .loading-icon {
          font-size: 48px;
          margin-bottom: 16px;
          animation: spin 1s linear infinite;
        }

        .loading-text {
          font-size: 14px;
          color: #c41e3a;
        }
      }

      .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 200px;
        color: #9ca3af;

        .empty-icon {
          color: #f2a5b5;
          margin-bottom: 16px;
        }

        .empty-text {
          font-size: 16px;
          font-weight: 600;
          color: #6b7280;
          letter-spacing: 0.2px;
          margin-bottom: 8px;
        }
      }

      .session-card {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 12px 16px;
        margin-bottom: 8px;
        border-radius: 12px;
        cursor: pointer;
        transition: all 0.2s ease;
        position: relative;
        border: 1px solid transparent;
        background-color: #fceef2;

        &:hover {
          background-color: #f8d0d8;
          border-color: #e87187;
          transform: translateY(-1px);
          box-shadow: 0 4px 12px rgba(196, 30, 58, 0.1);
        }

        &.active {
          background-color: #f8d0d8;
          border-color: #c41e3a;
          box-shadow: 0 4px 12px rgba(196, 30, 58, 0.15);

          .session-title {
            color: #c41e3a;
            font-weight: 600;
          }

          .session-icon {
            background: linear-gradient(135deg, #c41e3a, #d94560);
            color: white;
          }
        }

        .session-icon {
          flex-shrink: 0;
          width: 36px;
          height: 36px;
          display: flex;
          align-items: center;
          justify-content: center;
          background-color: #f2a5b5;
          border-radius: 10px;
          color: #c41e3a;
        }

        .session-info {
          flex: 1;
          min-width: 0;

          .session-title {
            font-size: 14px;
            color: #4a1a25;
            overflow: hidden;
            text-overflow: ellipsis;
            white-space: nowrap;
            margin-bottom: 4px;
          }

          .session-time {
            font-size: 11px;
            color: #d94560;
          }
        }

        .delete-btn {
          position: absolute;
          right: 12px;
          top: 50%;
          transform: translateY(-50%);
          width: 24px;
          height: 24px;
          display: flex;
          align-items: center;
          justify-content: center;
          background: rgba(255, 255, 255, 0.8);
          border: 1px solid #f2a5b5;
          border-radius: 6px;
          color: #d94560;
          opacity: 0;
          transition: all 0.2s ease;
          cursor: pointer;

          &:hover {
            background-color: #fee2e2;
            color: #ef4444;
            border-color: #ef4444;
          }
        }

        &:hover .delete-btn {
          opacity: 1;
        }
      }
    }
  }

  .content {
    flex: 1;
    overflow: hidden;
    background-color: #fceef2;
  }
}

@keyframes spin {
  from {
    transform: rotate(0deg);
  }
  to {
    transform: rotate(360deg);
  }
}

:deep(.el-dropdown-menu) {
  border: none;
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.12);
  border-radius: 8px;
  overflow: hidden;
  
  .el-dropdown-menu__item {
    padding: 12px 16px;
    font-size: 14px;
    
    &:hover {
      background-color: #f8d0d8;
      color: #c41e3a;
    }
    
    .el-icon {
      margin-right: 8px;
    }
  }
}

@media (max-width: 768px) {
  .workspace-nav {
    .nav-right {
      .nav-links {
        display: none;
      }
    }
  }

  .workspace-main {
    .sidebar {
      width: 240px;
    }
  }
}

@media (max-width: 480px) {
  .workspace-nav {
    padding: 0 12px;
  }

  .workspace-main {
    flex-direction: column;

    .sidebar {
      width: 100%;
      height: auto;
      max-height: 300px;
    }

    .content {
      flex: 1;
      margin: 0;
    }
  }
}
</style>
