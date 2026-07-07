<script setup lang="ts">
import { ref, onMounted, computed } from "vue"
import { useRouter } from "vue-router"
import { ElMessage, ElMessageBox } from "element-plus"
import { getAgentsAPI } from "../../apis/agent"
import { createDialogAPI, getDialogListAPI, deleteDialogAPI } from "../../apis/history"
import type { AgentResponse, ApiResponse } from "../../apis/agent"
import type { HistoryListType, DialogCreateType } from "../../type"
import histortCard from '../../components/historyCard/histortCard.vue'
import { useHistoryChatStore } from "../../store/history_chat_msg"

const router = useRouter()
const historyChatStore = useHistoryChatStore()
const searchKeyword = ref('')
const selectedDialog = ref('')
const showCreateDialog = ref(false)
const selectedAgent = ref('')
const agentSearchKeyword = ref('')

// 真实数据
const dialogs = ref<HistoryListType[]>([])
const agents = ref<AgentResponse[]>([])
const loading = ref(false)
const agentsLoading = ref(false)

// 过滤后的会话数据
const filteredDialogs = computed(() => {
  if (!searchKeyword.value) return dialogs.value
  return dialogs.value.filter(dialog => 
    dialog.name.toLowerCase().includes(searchKeyword.value.toLowerCase()) ||
    dialog.agent.toLowerCase().includes(searchKeyword.value.toLowerCase())
  )
})

// 过滤后的智能体数据
const filteredAgents = computed(() => {
  if (!agentSearchKeyword.value) return agents.value
  return agents.value.filter(agent => 
    agent.name.toLowerCase().includes(agentSearchKeyword.value.toLowerCase()) ||
    agent.description.toLowerCase().includes(agentSearchKeyword.value.toLowerCase())
  )
})

// 格式化时间
const formatTime = (timeStr: string) => {
  try {
    if (!timeStr) return '未知时间'
    
    // 处理不同的时间格式
    let date: Date
    if (typeof timeStr === 'string') {
      // 如果是ISO格式字符串
      if (timeStr.includes('T') || timeStr.includes('Z')) {
        date = new Date(timeStr)
      } else {
        // 尝试解析其他格式
        date = new Date(timeStr)
      }
    } else {
      date = new Date(timeStr)
    }
    
    // 检查日期是否有效
    if (isNaN(date.getTime())) {
      console.warn('无效的时间格式:', timeStr)
      return '未知时间'
    }
    
    const now = new Date()
    const diffInHours = (now.getTime() - date.getTime()) / (1000 * 60 * 60)
    
    if (diffInHours < 1) return '刚刚'
    if (diffInHours < 24) return `${Math.floor(diffInHours)}小时前`
    if (diffInHours < 24 * 7) return `${Math.floor(diffInHours / 24)}天前`
    return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
  } catch (error) {
    console.error('时间格式化错误:', error, '时间字符串:', timeStr)
    return '未知时间'
  }
}

// 获取智能体列表
const fetchAgents = async () => {
  try {
    agentsLoading.value = true
    const response = await getAgentsAPI()
    if (response.data.status_code === 200) {
      agents.value = response.data.data
      console.log('智能体列表获取成功:', agents.value)
      console.log('智能体ID详情:', agents.value.map(a => ({
        name: a.name,
        agent_id: a.agent_id,
        id: (a as any).id,
        agent_id_type: typeof a.agent_id,
        id_type: typeof (a as any).id
      })))
    } else {
      ElMessage.error(`获取智能体列表失败: ${response.data.status_message}`)
    }
  } catch (error) {
    console.error('获取智能体列表出错:', error)
    ElMessage.error('获取智能体列表失败，请检查网络连接')
  } finally {
    agentsLoading.value = false
  }
}

// 获取对话列表
const fetchDialogs = async () => {
  try {
    loading.value = true
    const response = await getDialogListAPI()
    if (response.data.status_code === 200) {
      // 处理返回的数据，确保字段名称正确
      console.log('原始对话数据:', response.data.data)
      dialogs.value = response.data.data.map((dialog: any) => {
        const processedDialog = {
          dialogId: dialog.dialog_id,
          name: dialog.name,
          agent: dialog.name, // 使用智能体名称作为显示
          createTime: dialog.create_time || dialog.update_time || new Date().toISOString(),
          logo: dialog.logo_url || 'https://via.placeholder.com/40x40/ff9f43/ffffff?text=AI'
        }
        console.log('处理后的对话数据:', processedDialog)
        return processedDialog
      })
      console.log('对话列表获取成功:', dialogs.value)
      
      // 如果会话列表不为空且当前路由是默认页面，立即自动打开第一个会话
      if (dialogs.value.length > 0 && router.currentRoute.value.name === 'defaultPage') {
        const firstDialog = dialogs.value[0]
        console.log('立即自动打开第一个会话:', firstDialog.dialogId, firstDialog.name)
        
        // 设置选中的会话
        selectedDialog.value = firstDialog.dialogId
        
        // 设置聊天store的状态
        historyChatStore.dialogId = firstDialog.dialogId
        historyChatStore.name = firstDialog.name
        historyChatStore.logo = firstDialog.logo
        
        // 立即跳转到聊天页面
        router.push({
          path: '/conversation/chatPage',
          query: {
            dialog_id: firstDialog.dialogId
          }
        })
      }
    } else {
      ElMessage.error(`获取对话列表失败: ${response.data.status_message}`)
    }
  } catch (error) {
    console.error('获取对话列表出错:', error)
    ElMessage.error('获取对话列表失败，请检查网络连接')
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  console.log('会话页面已加载')
  // 如果当前是会话主页面，先获取对话列表检查是否需要跳转
  if (router.currentRoute.value.path === '/conversation') {
    await fetchDialogs()
    // 如果没有自动跳转（说明没有会话），再获取智能体列表
    if (router.currentRoute.value.name === 'defaultPage') {
      await fetchAgents()
    }
  } else {
    // 如果是其他子页面，正常加载
    await Promise.all([fetchAgents(), fetchDialogs()])
  }
  // ElMessage.success('页面加载成功')
})

// 创建新会话
const createDialog = async () => {
  if (!selectedAgent.value) {
    ElMessage.warning('请选择一个智能体')
    return
  }
  
  // 支持多种ID字段查找
  const agent = agents.value.find(a => {
    const agentIdMatch = a.agent_id === selectedAgent.value || String(a.agent_id) === String(selectedAgent.value)
    const idMatch = (a as any).id === selectedAgent.value || String((a as any).id) === String(selectedAgent.value)
    return agentIdMatch || idMatch
  })
  
  if (agent) {
    try {
      const dialogData: DialogCreateType = {
        name: `与${agent.name}的对话`,
        agent_id: (agent as any).id || agent.agent_id, // 优先使用 id 字段
        agent_type: "Agent" // 默认为普通Agent类型
      }
      
      console.log('创建会话数据:', dialogData)
      console.log('发送到后端的数据:', {
        name: dialogData.name,
        agent_id: dialogData.agent_id,
        agent_type: dialogData.agent_type
      })
      const response = await createDialogAPI(dialogData)
      if (response.data.status_code === 200) {
        ElMessage.success('会话创建成功')
        
        // 获取新创建的会话ID
        const dialogId = response.data.data.dialog_id
        console.log('获取到的 dialogId:', dialogId)
        console.log('完整的 response.data.data:', response.data.data)
        
        // 重新获取对话列表
        await fetchDialogs()
        showCreateDialog.value = false
        selectedAgent.value = ''
        agentSearchKeyword.value = ''
        
        // 跳转到新创建的会话页面
        if (dialogId) {
          console.log('准备跳转到会话页面，dialogId:', dialogId)
          
          // 更新选中的会话状态
          selectedDialog.value = dialogId
          
          // 设置聊天store的状态
          historyChatStore.dialogId = dialogId
          historyChatStore.name = dialogData.name
          historyChatStore.logo = agent.logo_url || 'https://via.placeholder.com/40x40/ff9f43/ffffff?text=AI'
          
          router.push({
            path: '/conversation/chatPage',
            query: {
              dialog_id: dialogId
            }
          })
        } else {
          console.error('dialogId 为空，无法跳转')
        }
      } else {
        ElMessage.error(`创建会话失败: ${response.data.status_message}`)
      }
    } catch (error) {
      console.error('创建会话出错:', error)
      ElMessage.error('创建会话失败，请检查网络连接')
    }
  } else {
    ElMessage.error('未找到选中的智能体')
  }
}

// 删除会话
const deleteDialog = async (dialogId: string) => {
  console.log('删除会话被调用，dialogId:', dialogId)
  try {
    const response = await deleteDialogAPI(dialogId)
    if (response.data.status_code === 200) {
      ElMessage({
        message: '会话删除成功',
        type: 'success',
        duration: 3000,
        showClose: false
      })
      // 重新获取对话列表
      await fetchDialogs()
      if (selectedDialog.value === dialogId) {
        selectedDialog.value = ''
      }
    } else {
      ElMessage.error(`删除会话失败: ${response.data.status_message}`)
    }
  } catch (error) {
    console.error('删除会话出错:', error)
    ElMessage.error('删除会话失败，请检查网络连接')
  }
}

// 选择会话
const selectDialog = (dialogId: string) => {
  const dialog = dialogs.value.find(d => d.dialogId === dialogId)
  if (!dialog) {
    console.error('未找到会话:', dialogId)
    return
  }
  
  console.log('选择会话:', dialogId, dialog.name)
  selectedDialog.value = dialogId
  
  // 设置聊天store的状态
  historyChatStore.dialogId = dialogId
  historyChatStore.name = dialog.name
  historyChatStore.logo = dialog.logo
  
  // 跳转到聊天页面
  router.push({
    path: '/conversation/chatPage',
    query: {
      dialog_id: dialogId
    }
  })
}

// 打开创建对话框
const openCreateDialog = async () => {
  showCreateDialog.value = true
  selectedAgent.value = ''
  agentSearchKeyword.value = ''
  
  // 如果智能体列表为空，重新获取
  if (agents.value.length === 0) {
    await fetchAgents()
  }
  
  // ElMessage.info('正在打开创建会话对话框...')
}

// 选择智能体
const selectAgent = (agentId: string) => {
  console.log('选择智能体:', agentId)
  console.log('当前智能体列表:', agents.value.map(a => ({ 
    agent_id: a.agent_id, 
    id: (a as any).id, 
    name: a.name 
  })))
  
  // 支持多种ID字段
  const agent = agents.value.find(a => {
    const agentIdMatch = a.agent_id === agentId || String(a.agent_id) === String(agentId)
    const idMatch = (a as any).id === agentId || String((a as any).id) === String(agentId)
    return agentIdMatch || idMatch
  })
  
  if (agent) {
    // 优先使用 id 字段作为选中值
    selectedAgent.value = (agent as any).id || agent.agent_id
    console.log('选中智能体:', agent.name, 'ID:', selectedAgent.value)
  } else {
    console.error('未找到智能体:', agentId)
  }
}

// 关闭创建对话框
const closeCreateDialog = () => {
  showCreateDialog.value = false
  selectedAgent.value = ''
  agentSearchKeyword.value = ''
}
</script>

<template>
  <div class="conversation-main">
    <!-- 左侧边栏 -->
    <div class="sidebar">
      <!-- 新建会话按钮 -->
      <div class="create-section">
        <button 
          @click="openCreateDialog"
          class="create-btn-native"
        >
          <div class="btn-content">
            <span class="icon">+</span>
            <span>新建会话</span>
          </div>
        </button>
      </div>

      

      <!-- 会话列表标题 -->
      <div class="list-header">
        <span class="title">会话列表</span>
        <span class="count">({{ filteredDialogs.length }})</span>
      </div>

      <!-- 会话列表 -->
      <div class="dialog-list">
        <!-- 加载状态 -->
        <div v-if="loading" class="loading-state">
          <div class="loading-icon">⏳</div>
          <div class="loading-text">正在加载会话列表...</div>
        </div>
        <!-- 空状态 -->
        <div v-else-if="filteredDialogs.length === 0" class="empty-state">
          <div class="empty-icon">💬</div>
          <div class="empty-text">
            {{ searchKeyword ? '没有找到相关会话' : '暂无会话记录' }}
          </div>
          <div v-if="!searchKeyword" class="empty-hint">
            点击上方按钮开始新的对话
          </div>
        </div>
        <!-- 用 histortCard 渲染会话卡片 -->
        <histortCard
          v-for="dialog in filteredDialogs" 
          :key="dialog.dialogId"
          :item="dialog"
          :class="{ active: selectedDialog === dialog.dialogId }"
          @select="selectDialog(dialog.dialogId)"
          @delete="deleteDialog(dialog.dialogId)"
        />
      </div>
    </div>

    <!-- 右侧内容区域，改为路由驱动 -->
    <div class="content">
      <router-view />
    </div>

    <!-- 创建会话对话框 -->
    <div v-if="showCreateDialog" class="create-dialog-overlay" @click="closeCreateDialog">
      <div class="create-dialog" @click.stop>
        <div class="dialog-header">
          <h3>选择智能体创建会话</h3>
          <button @click="closeCreateDialog" class="close-btn">×</button>
        </div>
        
        <div class="dialog-body">
          <!-- 智能体搜索框 -->
          <div class="search-section">
            <input
              v-model="agentSearchKeyword"
              placeholder="搜索智能体..."
              class="search-input"
            />
          </div>

          <!-- 智能体列表 -->
          <div class="agents-section">
            <div class="section-header">
              <span class="title">可用智能体</span>
              <span class="count">({{ filteredAgents.length }})</span>
            </div>

            <!-- 加载状态 -->
            <div v-if="agentsLoading" class="loading-state">
              <div class="loading-icon">⏳</div>
              <div class="loading-text">正在加载智能体列表...</div>
            </div>

            <!-- 空状态 -->
            <div v-else-if="filteredAgents.length === 0" class="empty-state">
              <div class="empty-icon">🤖</div>
              <div class="empty-text">
                {{ agentSearchKeyword ? '没有找到相关智能体' : '暂无可用智能体' }}
              </div>
              <div v-if="!agentSearchKeyword" class="empty-hint">
                请联系管理员添加智能体
              </div>
            </div>

            <div v-else class="agents-grid">
              <div
                v-for="agent in filteredAgents"
                :key="(agent as any).id || agent.agent_id"
                :class="['agent-card', selectedAgent === ((agent as any).id || agent.agent_id) ? 'active' : '']"
                @click="selectAgent((agent as any).id || agent.agent_id)"
              >
                <div class="agent-avatar">
                  <img :src="agent.logo_url" alt="" />
                </div>
                <div class="agent-info">
                  <div class="agent-name">{{ agent.name }}</div>
                  <div class="agent-description">{{ agent.description }}</div>
                </div>
                <div class="agent-status">
                  <div v-if="selectedAgent === ((agent as any).id || agent.agent_id)" class="selected-icon">
                    ★
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="dialog-footer">
          <div class="debug-info" style="font-size: 12px; color: #666; margin-bottom: 8px;">
            当前选中: {{ selectedAgent ? agents.find(a => (a.agent_id === selectedAgent || (a as any).id === selectedAgent))?.name || selectedAgent : '无' }}
          </div>
          <button @click="closeCreateDialog" class="btn-cancel">取消</button>
          <button 
            @click="createDialog"
            :disabled="!selectedAgent"
            class="btn-confirm"
          >
            创建会话
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.conversation-main {
  display: flex;
  height: calc(100vh - 60px);
  background-color: var(--newsprint-bg);

  .sidebar {
    height: 100%;
    width: 280px;
    background-color: var(--newsprint-bg);
    border-right: 1px solid var(--newsprint-border);
    display: flex;
    flex-direction: column;

    .create-section {
      padding: 20px 16px 16px;
      border-bottom: 1px solid var(--newsprint-border);

      .create-btn-native {
        width: 100%;
        height: 48px;
        font-weight: 600;
        transition: all 0.2s ease;
        background: var(--newsprint-fg);
        color: var(--newsprint-bg);
        border: 2px solid var(--newsprint-fg);
        cursor: pointer;
        font-size: 14px;
        text-transform: uppercase;
        letter-spacing: 0.05em;

        &:hover {
          background: var(--newsprint-bg);
          color: var(--newsprint-fg);
          box-shadow: 4px 4px 0px 0px var(--newsprint-fg);
          transform: translate(-2px, -2px);
        }

        &:active {
          transform: translate(0, 0);
          box-shadow: 0 0 0 0 var(--newsprint-fg);
        }

        .btn-content {
          display: flex;
          align-items: center;
          justify-content: center;
          gap: 8px;

          .icon {
            font-size: 18px;
            font-weight: bold;
          }
        }
      }
    }

    .search-section {
      padding: 16px;
      border-bottom: 1px solid var(--newsprint-border);

      .search-input-wrapper {
        position: relative;
        display: flex;
        align-items: center;

        .search-icon {
          position: absolute;
          left: 12px;
          color: var(--newsprint-fg);
          font-size: 14px;
          z-index: 1;
        }

        .search-input {
          width: 100%;
          padding: 10px 12px 10px 36px;
          border: none;
          border-bottom: 2px solid var(--newsprint-border);
          font-size: 14px;
          background: transparent;
          transition: all 0.2s ease;
          color: var(--newsprint-fg);
          font-family: 'JetBrains Mono', monospace;

          &:focus {
            outline: none;
            border-color: var(--newsprint-accent);
            background: #F0F0F0;
          }

          &::placeholder {
            color: var(--newsprint-neutral-400);
          }
        }
      }
    }

    .list-header {
      padding: 16px 16px 8px;
      display: flex;
      align-items: center;
      gap: 4px;

      .title {
        font-size: 14px;
        font-weight: 600;
        color: var(--newsprint-fg);
        text-transform: uppercase;
        letter-spacing: 0.1em;
      }

      .count {
        font-size: 12px;
        color: var(--newsprint-neutral-500);
        font-family: 'JetBrains Mono', monospace;
      }
    }

    .dialog-list {
      flex: 1;
      padding: 0 8px;
      overflow-y: auto;

      .loading-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 200px;

        .loading-icon {
          font-size: 48px;
          margin-bottom: 16px;
          animation: spin 1s linear infinite;
        }

        .loading-text {
          font-size: 14px;
          color: var(--newsprint-neutral-500);
        }
      }

      .empty-state {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
        height: 200px;

        .empty-icon {
          font-size: 48px;
          margin-bottom: 16px;
        }

        .empty-text {
          font-size: 14px;
          margin-bottom: 8px;
          color: var(--newsprint-neutral-500);
        }

        .empty-hint {
          font-size: 12px;
          color: var(--newsprint-accent);
        }
      }

      .dialog-card {
        background: var(--newsprint-bg);
        border: 1px solid var(--newsprint-border);
        padding: 16px;
        margin-bottom: 8px;
        cursor: pointer;
        transition: all 0.2s ease;
        min-height: 80px;
        position: relative;

        &:hover {
          border-color: var(--newsprint-accent);
          box-shadow: 4px 4px 0px 0px var(--newsprint-border);
          transform: translate(-2px, -2px);
        }

        &.active {
          border-color: var(--newsprint-accent);
          background-color: var(--newsprint-neutral-100);
          border-left: 3px solid var(--newsprint-accent);
        }

        .avatar {
          position: absolute;
          top: 16px;
          left: 16px;
          width: 40px;
          height: 40px;
          overflow: hidden;
          border: 1px solid var(--newsprint-border);

          img {
            width: 100%;
            height: 100%;
            object-fit: cover;
          }
        }

        .title {
          position: absolute;
          top: 16px;
          left: 68px;
          right: 60px;
          font-size: 14px;
          font-weight: 600;
          color: var(--newsprint-fg);
          overflow: hidden;
          text-overflow: ellipsis;
          white-space: nowrap;
        }

        .delete-btn {
          position: absolute;
          top: 16px;
          right: 16px;
          width: 32px;
          height: 32px;
          padding: 4px;
          background: transparent;
          border: 1px solid var(--newsprint-border);
          cursor: pointer;
          transition: all 0.2s ease;
          font-size: 14px;
          opacity: 0;
          z-index: 10;
          display: flex;
          align-items: center;
          justify-content: center;
          user-select: none;
          pointer-events: auto;
          outline: none;

          &:hover {
            background: var(--newsprint-fg);
            color: var(--newsprint-bg);
            border-color: var(--newsprint-fg);
            opacity: 1;
          }

          &:active {
            transform: scale(0.95);
          }
        }

        &:hover .delete-btn {
          opacity: 1 !important;
        }

        .time {
          position: absolute;
          bottom: 8px;
          right: 16px;
          font-size: 11px;
          color: var(--newsprint-neutral-500);
          font-family: 'JetBrains Mono', monospace;
        }
      }
    }
  }

  .content {
    flex: 1;
    background-color: var(--newsprint-bg);
    border-left: 1px solid var(--newsprint-border);
    overflow: hidden;

    .welcome-content {
      flex: 1;
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      text-align: center;
      color: var(--newsprint-neutral-500);
      height: 100%;

      .welcome-icon {
        margin-bottom: 24px;

        .icon {
          font-size: 48px;
          color: var(--newsprint-fg);
        }
      }

      h2 {
        font-size: 1.5rem;
        margin: 0 0 12px 0;
        color: var(--newsprint-fg);
        font-weight: 700;
        font-family: 'Playfair Display', serif;
      }

      p {
        font-size: 1rem;
        margin: 0;
        color: var(--newsprint-neutral-500);
      }
    }

    .chat-content {
      flex: 1;
      display: flex;
      flex-direction: column;

      .chat-header {
        padding: 20px;
        border-bottom: 1px solid var(--newsprint-border);
        background: var(--newsprint-neutral-100);

        h3 {
          margin: 0;
          color: var(--newsprint-fg);
          font-weight: 600;
        }
      }

      .chat-messages {
        flex: 1;
        padding: 20px;
        background-color: var(--newsprint-bg);

        .message {
          padding: 12px 16px;
          margin-bottom: 12px;
          border: 1px solid var(--newsprint-border);

          &.system {
            background: var(--newsprint-neutral-100);
            color: var(--newsprint-neutral-500);
          }
        }
      }
    }
  }
}

.dialog-content {
  .search-section {
    margin-bottom: 20px;
  }

  .agents-section {
    .section-header {
      display: flex;
      align-items: center;
      gap: 4px;
      margin-bottom: 16px;

      .title {
        font-size: 16px;
        font-weight: 600;
        color: var(--newsprint-fg);
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }

      .count {
        font-size: 14px;
        color: var(--newsprint-neutral-500);
        font-family: 'JetBrains Mono', monospace;
      }
    }

    .empty-state {
      text-align: center;
      padding: 40px 20px;
      color: var(--newsprint-neutral-500);

      .empty-icon {
        font-size: 48px;
        margin-bottom: 16px;
      }

      .empty-text {
        font-size: 14px;
        margin-bottom: 8px;
      }

      .empty-hint {
        font-size: 12px;
        color: var(--newsprint-accent);
      }
    }

    .agents-grid {
      display: grid;
      gap: 12px;
      max-height: 400px;
      overflow-y: auto;

      .agent-card {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 16px;
        border: 1px solid var(--newsprint-border);
        cursor: pointer;
        transition: all 0.2s ease;
        position: relative;

        &:hover {
          background: var(--newsprint-neutral-100);
          border-color: var(--newsprint-accent);
        }

        &.active {
          border-color: var(--newsprint-accent);
          background: var(--newsprint-neutral-100);
          border-left: 3px solid var(--newsprint-accent);
        }

        .agent-avatar {
          width: 48px;
          height: 48px;
          overflow: hidden;
          flex-shrink: 0;
          border: 1px solid var(--newsprint-border);

          img {
            width: 100%;
            height: 100%;
            object-fit: cover;
          }
        }

        .agent-info {
          flex: 1;

          .agent-name {
            font-size: 16px;
            font-weight: 600;
            color: var(--newsprint-fg);
            margin-bottom: 4px;
          }

          .agent-description {
            font-size: 14px;
            color: var(--newsprint-neutral-500);
            line-height: 1.4;
          }
        }

        .agent-status {
          flex-shrink: 0;

          .selected-icon {
            width: 24px;
            height: 24px;
            display: flex;
            align-items: center;
            justify-content: center;
            background: var(--newsprint-fg);
            color: var(--newsprint-bg);
          }
        }
      }
    }
  }
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  padding-top: 16px;
  border-top: 1px solid var(--newsprint-border);
}

// 响应式设计
@media (max-width: 768px) {
  .conversation-main {
    .sidebar {
      width: 240px;
    }
    
    .content {
      margin: 0;
    }
  }
}

@media (max-width: 480px) {
  .conversation-main {
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

// 原生对话框样式
.create-dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(17, 17, 17, 0.4);
  backdrop-filter: blur(4px);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease;
}

.create-dialog {
  background: var(--newsprint-bg);
  width: 600px;
  max-width: 90vw;
  max-height: 85vh;
  overflow: hidden;
  box-shadow: 8px 8px 0px 0px var(--newsprint-fg);
  animation: slideIn 0.3s ease;
  display: flex;
  flex-direction: column;
  border: 2px solid var(--newsprint-fg);

  .dialog-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: 24px 24px 16px;
    border-bottom: 1px solid var(--newsprint-border);
    background: var(--newsprint-neutral-100);

    h3 {
      margin: 0;
      color: var(--newsprint-fg);
      font-size: 18px;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }

    .close-btn {
      background: none;
      border: 1px solid var(--newsprint-border);
      font-size: 24px;
      cursor: pointer;
      color: var(--newsprint-neutral-500);
      padding: 0;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      transition: all 0.2s ease;

      &:hover {
        background: var(--newsprint-fg);
        color: var(--newsprint-bg);
        border-color: var(--newsprint-fg);
      }
    }
  }

  .dialog-body {
    flex: 1;
    padding: 20px 24px;
    overflow-y: auto;
    background-color: var(--newsprint-bg);

    .search-section {
      margin-bottom: 20px;

      .search-input {
        width: 100%;
        padding: 12px 16px;
        border: none;
        border-bottom: 2px solid var(--newsprint-border);
        font-size: 14px;
        transition: all 0.2s ease;
        background: transparent;
        color: var(--newsprint-fg);
        font-family: 'JetBrains Mono', monospace;

        &:focus {
          outline: none;
          border-color: var(--newsprint-accent);
          background: #F0F0F0;
        }

        &::placeholder {
          color: var(--newsprint-neutral-400);
        }
      }
    }

    .agents-section {
      .section-header {
        display: flex;
        align-items: center;
        gap: 8px;
        margin-bottom: 16px;

        .title {
          font-size: 16px;
          font-weight: 600;
          color: var(--newsprint-fg);
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .count {
          font-size: 14px;
          color: var(--newsprint-neutral-500);
          background: var(--newsprint-neutral-100);
          padding: 2px 8px;
          border: 1px solid var(--newsprint-border);
          font-weight: 600;
          font-family: 'JetBrains Mono', monospace;
        }
      }

      .empty-state {
        text-align: center;
        padding: 40px 20px;
        color: var(--newsprint-neutral-500);

        .empty-icon {
          font-size: 48px;
          margin-bottom: 16px;
        }

        .empty-text {
          font-size: 14px;
          margin-bottom: 8px;
          color: var(--newsprint-neutral-500);
        }

        .empty-hint {
          font-size: 12px;
          color: var(--newsprint-accent);
        }
      }

      .agents-grid {
        display: grid;
        gap: 12px;
        max-height: 400px;
        overflow-y: auto;

        .agent-card {
          display: flex;
          align-items: center;
          gap: 12px;
          padding: 16px;
          border: 1px solid var(--newsprint-border);
          cursor: pointer;
          transition: all 0.2s ease;
          position: relative;
          background: var(--newsprint-bg);

          &:hover {
            border-color: var(--newsprint-accent);
            box-shadow: 4px 4px 0px 0px var(--newsprint-border);
            transform: translate(-2px, -2px);
          }

          &.active {
            border-color: var(--newsprint-accent);
            background: var(--newsprint-neutral-100);
            border-left: 3px solid var(--newsprint-accent);
          }

          .agent-avatar {
            width: 48px;
            height: 48px;
            overflow: hidden;
            flex-shrink: 0;
            border: 1px solid var(--newsprint-border);

            img {
              width: 100%;
              height: 100%;
              object-fit: cover;
            }
          }

          .agent-info {
            flex: 1;

            .agent-name {
              font-size: 16px;
              font-weight: 600;
              color: var(--newsprint-fg);
              margin-bottom: 4px;
            }

            .agent-description {
              font-size: 14px;
              color: var(--newsprint-neutral-500);
              line-height: 1.4;
            }
          }

          .agent-status {
            flex-shrink: 0;

            .selected-icon {
              width: 24px;
              height: 24px;
              display: flex;
              align-items: center;
              justify-content: center;
              background: var(--newsprint-fg);
              color: var(--newsprint-bg);
              font-size: 12px;
            }
          }
        }
      }
    }
  }

  .dialog-footer {
    display: flex;
    justify-content: flex-end;
    gap: 12px;
    padding: 16px 24px;
    border-top: 1px solid var(--newsprint-border);
    background: var(--newsprint-neutral-100);

    .btn-cancel {
      padding: 10px 24px;
      border: 1px solid var(--newsprint-border);
      background: var(--newsprint-bg);
      color: var(--newsprint-neutral-500);
      cursor: pointer;
      font-size: 14px;
      transition: all 0.2s ease;
      text-transform: uppercase;
      letter-spacing: 0.05em;

      &:hover {
        background: var(--newsprint-neutral-100);
        color: var(--newsprint-fg);
        border-color: var(--newsprint-fg);
      }
    }

    .btn-confirm {
      padding: 10px 24px;
      border: 2px solid var(--newsprint-fg);
      background: var(--newsprint-fg);
      color: var(--newsprint-bg);
      cursor: pointer;
      font-size: 14px;
      font-weight: 600;
      transition: all 0.2s ease;
      text-transform: uppercase;
      letter-spacing: 0.05em;

      &:hover:not(:disabled) {
        background: var(--newsprint-bg);
        color: var(--newsprint-fg);
        box-shadow: 4px 4px 0px 0px var(--newsprint-fg);
        transform: translate(-2px, -2px);
      }

      &:disabled {
        background: var(--newsprint-fg);
        opacity: 0.5;
        cursor: not-allowed;
        transform: none;
        box-shadow: none;
      }
    }
  }
}

// 动画
@keyframes fadeIn {
  from {
    opacity: 0;
  }
  to {
    opacity: 1;
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(-20px);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0);
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
</style>
