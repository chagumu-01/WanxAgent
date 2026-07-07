<script setup lang="ts">
import AgentCard from "../../components/agentCard/index"
import { onMounted, ref } from "vue"
import { useRouter } from "vue-router"
import { Agent } from "../../type"
import { getAgentsAPI } from "../../apis/agent"


const router = useRouter()
const cardList = ref<Agent[]>([])


const openDialog = (event: string, item?: Agent) => {
  if (event === "create") {
    // 创建智能体时跳转到编辑页面
    createAgent()
  } else {
    // 编辑智能体时跳转到编辑页面
    editAgent(item!)
  }
}

// 创建智能体 - 跳转到编辑页面
const createAgent = () => {
  router.push('/agent/editor')
}

// 编辑智能体 - 跳转到编辑页面
const editAgent = (agent: Agent) => {
  router.push({
    path: '/agent/editor',
    query: { id: agent.agent_id }
  })
}

const updateList = async () => {
  try {
    const response = await getAgentsAPI()
    cardList.value = response.data.data
  } catch (error) {
    console.error('获取智能体列表失败:', error)
  }
}

onMounted(async () => {
  updateList()
})

</script>

<template>
  <div class="agent-card">
    <div class="create" @click="openDialog('create')">
      <div class="content">
        <div class="top">
          <img src="../../assets/plugin.svg" alt="" width="40px" height="40px" />
          <span>新建助手</span>
        </div>
        <div class="middle">
          通过描述角色和任务来创建你的助手<br />
          助手可以调用多个技能和工具
        </div>
      </div>
    </div>
    <div v-for="item in cardList" :key="item.agent_id">
      <AgentCard
        :item="item"
        @delete="updateList"
        @edit="editAgent"
        @click="openDialog('update', item)"
      ></AgentCard>
    </div>

  </div>
</template>

<style lang="scss" scoped>
.agent-card {
  padding: 32px;
  min-height: calc(100vh - 150px);
  background: var(--newsprint-bg);
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(220px, 1fr));
  gap: 16px;
  
  .create {
    margin: 0;
    padding: 0;
    display: flex;
    flex-direction: column;
    height: 160px;
    background: var(--newsprint-fg);
    border-radius: 4px;
    border: 2px solid var(--newsprint-fg);
    box-shadow: 4px 4px 0px 0px var(--newsprint-border);
    transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
    cursor: pointer;
    position: relative;
    overflow: hidden;

          .content {
        padding: 16px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        height: 100%;
        position: relative;
        z-index: 1;

        .top {
          display: flex;
          align-items: center;
          margin-bottom: 12px;
          
          img {
            width: 40px;
            height: 40px;
            margin-right: 12px;
            filter: brightness(0) invert(1);
            transition: all 0.3s ease;
          }
          
          span {
            font-size: 18px;
            font-weight: 600;
            color: white;
            font-family: 'Playfair Display', serif;
            text-transform: uppercase;
            letter-spacing: 0.05em;
          }
        }

        .middle {
          font-size: 14px;
          font-weight: 400;
          line-height: 1.5;
          color: rgba(255, 255, 255, 0.9);
          font-family: 'Lora', serif;
        }
      }
    
    &:hover {
      transform: translate(-2px, -2px);
      box-shadow: 8px 8px 0px 0px var(--newsprint-border);
      
      .content {
        .top img {
          transform: scale(1.1) rotate(5deg);
          filter: brightness(0) invert(1);
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 1200px) {
  .agent-card {
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 20px;
    padding: 24px;
  }
}

@media (max-width: 768px) {
  .agent-card {
    grid-template-columns: 1fr;
    gap: 16px;
    padding: 16px;
    
    .create {
      height: 180px;
      
      .content {
        padding: 24px;
        
        .top {
          span {
            font-size: 20px;
          }
          
          img {
            width: 40px;
            height: 40px;
          }
        }
        
        .middle {
          font-size: 14px;
        }
      }
    }
  }
}
</style>
