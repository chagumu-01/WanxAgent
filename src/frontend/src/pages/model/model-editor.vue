<script setup lang="ts">
import { ref, onMounted, reactive } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { ArrowLeft, Check, Close, Setting, Cpu } from '@element-plus/icons-vue'
import type { FormInstance, FormRules } from 'element-plus'
import { 
  getVisibleLLMsAPI, 
  updateLLMAPI, 
  deleteLLMAPI, 
  getLLMSchemaAPI,
  type LLMResponse,
  type UpdateLLMRequest
} from '../../apis/llm'

const router = useRouter()
const route = useRoute()

// 响应式数据
const loading = ref(false)
const currentModel = ref<LLMResponse | null>(null)

// 表单相关
const editFormRef = ref<FormInstance>()

const editForm = reactive<UpdateLLMRequest>({
  llm_id: '',
  model: '',
  api_key: '',
  base_url: '',
  provider: '',
  llm_type: ''
})

// 模型类型选项
const llmTypeOptions = [
  { label: 'LLM', value: 'LLM' },
  { label: 'Embedding', value: 'Embedding' },
  { label: 'Rerank', value: 'Rerank' }
]

// 表单验证规则
const formRules: FormRules = {
  model: [
    { required: true, message: '请输入模型名称', trigger: 'blur' }
  ],
  api_key: [
    { required: true, message: '请输入API密钥', trigger: 'blur' }
  ],
  base_url: [
    { required: true, message: '请输入基础URL', trigger: 'blur' }
  ],
  provider: [
    { required: true, message: '请输入提供商', trigger: 'blur' }
  ],
  llm_type: [
    { required: true, message: '请选择模型类型', trigger: 'change' }
  ]
}

// 获取模型详情
const fetchModelDetail = async () => {
  const modelId = route.query.id as string
  if (!modelId) {
    ElMessage.error('缺少模型ID参数')
    router.push('/model')
    return
  }

  loading.value = true
  try {
    const response = await getVisibleLLMsAPI()
    
    if (response.data.status_code === 200) {
      const data = response.data.data || {}
      const allModels: LLMResponse[] = []
      
      Object.values(data).forEach((typeModels: any) => {
        if (Array.isArray(typeModels)) {
          allModels.push(...typeModels)
        }
      })
      
      const targetModel = allModels.find(model => model.llm_id === modelId)
      if (targetModel) {
        // 检查是否为官方模型
        if (targetModel.user_id === '0') {
          ElMessage.warning('官方模型不可编辑，请返回模型列表')
          setTimeout(() => {
            router.push('/model')
          }, 1500)
          return
        }
        
        currentModel.value = targetModel
        // 填充表单
        Object.assign(editForm, {
          llm_id: targetModel.llm_id,
          model: targetModel.model,
          api_key: targetModel.api_key,
          base_url: targetModel.base_url,
          provider: targetModel.provider,
          llm_type: targetModel.llm_type
        })
      } else {
        ElMessage.error('未找到指定的模型')
        router.push('/model')
      }
    } else {
      ElMessage.error(response.data.status_message || '获取模型详情失败')
      router.push('/model')
    }
  } catch (error) {
    ElMessage.error('获取模型详情失败')
    console.error('获取模型详情失败:', error)
    router.push('/model')
  } finally {
    loading.value = false
  }
}

// 返回模型管理页面
const goBack = () => {
  router.push('/model')
}

// 更新模型
const handleUpdate = async () => {
  if (!editFormRef.value) return
  
  try {
    await editFormRef.value.validate()
    const response = await updateLLMAPI(editForm)
    
    if (response.data.status_code === 200) {
      ElMessage.success('更新成功')
      router.push('/model')
    } else {
      ElMessage.error(response.data.status_message || '更新失败')
    }
  } catch (error) {
    ElMessage.error('更新失败')
    console.error('更新模型失败:', error)
  }
}

// 删除模型
const handleDelete = async () => {
  if (!currentModel.value) return
  
  // 检查是否为官方模型
  if (currentModel.value.user_id === '0') {
    ElMessage.warning('⚠️ 官方模型不可删除')
    return
  }
  
  try {
    await ElMessageBox.confirm(
      `确定要删除模型"${currentModel.value.model}"吗？删除后无法恢复。`,
      '确认删除',
      {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning',
      }
    )
    
    const response = await deleteLLMAPI({ llm_id: currentModel.value.llm_id })
    
    if (response.data.status_code === 200) {
      ElMessage.success('删除成功')
      router.push('/model')
    } else {
      ElMessage.error(response.data.status_message || '删除失败')
    }
  } catch (error: any) {
    if (error !== 'cancel') {
      console.error('删除模型失败:', error)
      ElMessage.error('删除失败')
    }
  }
}

// 测试模型连接
const testModel = async () => {
  if (!currentModel.value) return
  
  ElMessage.info(`正在测试 ${currentModel.value.model} 连接...`)
  // 这里可以添加实际的测试逻辑
  setTimeout(() => {
    ElMessage.success(`${currentModel.value!.model} 连接测试完成`)
  }, 2000)
}

onMounted(() => {
  fetchModelDetail()
})
</script>

<template>
  <div class="model-editor-page" v-loading="loading">
    <!-- 页面头部 -->
    <div class="page-header">
      <div class="header-left">
        <div class="breadcrumb">
          <span class="breadcrumb-item clickable" @click="goBack">模型管理</span>
          <span class="breadcrumb-separator">></span>
          <span class="breadcrumb-item active">编辑模型</span>
        </div>
      </div>
      
      <div class="header-title">
        <div class="title-icon">
          <el-icon><Setting /></el-icon>
        </div>
        <h2>编辑模型</h2>
      </div>
    </div>

    <!-- 编辑表单 -->
    <div v-if="currentModel" class="edit-form-section">
      <div class="form-container">
        <div class="form-header">
          <div class="form-icon">
            <el-icon><Cpu /></el-icon>
          </div>
          <div class="form-title">
            <h3>模型配置</h3>
            <p>修改模型的基本信息和连接配置</p>
          </div>
        </div>
        
        <el-form
          ref="editFormRef"
          :model="editForm"
          :rules="formRules"
          label-width="120px"
          label-position="left"
          class="edit-form"
        >
          <div class="form-section">
            <h4 class="section-title">基本信息</h4>
            <div class="form-row">
              <el-form-item label="模型名称" prop="model">
                <el-input 
                  v-model="editForm.model" 
                  placeholder="请输入模型名称，如：gpt-4"
                  clearable
                  maxlength="50"
                  show-word-limit
                  class="form-input"
                />
              </el-form-item>
              
              <el-form-item label="提供商" prop="provider">
                <el-input 
                  v-model="editForm.provider" 
                  placeholder="请输入提供商，如：OpenAI"
                  clearable
                  maxlength="50"
                  show-word-limit
                  class="form-input"
                />
              </el-form-item>
            </div>
            
            <div class="form-row">
              <el-form-item label="模型类型" prop="llm_type">
                <el-select 
                  v-model="editForm.llm_type" 
                  placeholder="请选择模型类型"
                  class="form-select"
                  clearable
                >
                  <el-option
                    v-for="option in llmTypeOptions"
                    :key="option.value"
                    :label="option.label"
                    :value="option.value"
                  />
                </el-select>
              </el-form-item>
            </div>
          </div>
          
          <div class="form-section">
            <h4 class="section-title">连接配置</h4>
            <div class="form-row">
              <el-form-item label="基础URL" prop="base_url">
                <el-input 
                  v-model="editForm.base_url" 
                  placeholder="请输入基础URL，如：https://api.openai.com/v1"
                  clearable
                  maxlength="200"
                  show-word-limit
                  class="form-input"
                />
              </el-form-item>
            </div>
            
            <div class="form-row">
              <el-form-item label="API密钥" prop="api_key">
                <el-input 
                  v-model="editForm.api_key" 
                  placeholder="请输入API密钥"
                  type="password"
                  show-password
                  clearable
                  maxlength="200"
                  show-word-limit
                  class="form-input"
                />
              </el-form-item>
            </div>
          </div>
          
          <el-form-item>
            <div class="form-actions">
              <el-button @click="goBack" class="action-btn cancel-btn">
                <el-icon><Close /></el-icon>
                取消
              </el-button>
              <el-button 
                type="primary" 
                @click="handleUpdate"
                class="action-btn primary-btn"
              >
                <el-icon><Check /></el-icon>
                保存更改
              </el-button>
            </div>
          </el-form-item>
        </el-form>
      </div>
    </div>

    <!-- 空状态 -->
    <div v-else-if="!loading" class="empty-state">
      <div class="empty-icon">
        <el-icon><Close /></el-icon>
      </div>
      <h3>未找到模型</h3>
      <p>请检查模型ID是否正确</p>
      <el-button 
        type="primary" 
        :icon="ArrowLeft"
        @click="goBack"
        size="large"
      >
        返回模型管理
      </el-button>
    </div>
  </div>
</template>

<style lang="scss" scoped>
.model-editor-page {
  padding: 24px;
  height: 100%;
  background-color: var(--newsprint-bg);
  min-height: 100vh;
  
  .page-header {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 32px;
    background: var(--newsprint-bg);
    padding: 24px 32px;
    box-shadow: 4px 4px 0px 0px var(--newsprint-border);
    border: 1px solid var(--newsprint-border);
    
    .header-left {
      display: flex;
      align-items: center;
      gap: 20px;
      
      .breadcrumb {
        display: flex;
        align-items: center;
        gap: 12px;
        font-size: 15px;
        color: var(--newsprint-neutral-500);
        
        .breadcrumb-item {
          transition: all 0.2s ease;
          padding: 8px 12px;
          border: 1px solid transparent;
          cursor: default;
          font-family: 'Lora', serif;
          
          &.clickable {
            cursor: pointer;
            color: var(--newsprint-neutral-500);
            font-weight: 500;
            border-color: var(--newsprint-border);
            background: var(--newsprint-neutral-100);
            
            &:hover {
              color: var(--newsprint-fg);
              background: var(--newsprint-border);
            }
          }
          
          &.active {
            color: var(--newsprint-accent);
            font-weight: 600;
            border-color: var(--newsprint-accent);
            background: var(--newsprint-bg);
          }
        }
        
        .breadcrumb-separator {
          color: var(--newsprint-neutral-400);
          font-weight: 500;
        }
      }
    }
    
    .header-title {
      display: flex;
      align-items: center;
      gap: 16px;
      
      .title-icon {
        width: 48px;
        height: 48px;
        background: var(--newsprint-fg);
        display: flex;
        align-items: center;
        justify-content: center;
        
        .el-icon {
          font-size: 24px;
          color: var(--newsprint-bg);
        }
      }
      
      h2 {
        margin: 0;
        font-size: 28px;
        font-weight: 700;
        color: var(--newsprint-fg);
        font-family: 'Playfair Display', serif;
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }
    }
  }
  
  .edit-form-section {
    .form-container {
      background: var(--newsprint-bg);
      padding: 32px;
      box-shadow: 4px 4px 0px 0px var(--newsprint-border);
      border: 1px solid var(--newsprint-border);
      
      .form-header {
        display: flex;
        align-items: center;
        gap: 20px;
        margin-bottom: 32px;
        padding-bottom: 24px;
        border-bottom: 2px solid var(--newsprint-border);
        
        .form-icon {
          width: 56px;
          height: 56px;
          background: var(--newsprint-fg);
          display: flex;
          align-items: center;
          justify-content: center;
          
          .el-icon {
            font-size: 28px;
            color: var(--newsprint-bg);
          }
        }
        
        .form-title {
          h3 {
            margin: 0 0 12px 0;
            font-size: 28px;
            font-weight: 700;
            color: var(--newsprint-fg);
            font-family: 'Playfair Display', serif;
            text-transform: uppercase;
            letter-spacing: 0.05em;
          }
          
          p {
            margin: 0;
            font-size: 16px;
            color: var(--newsprint-neutral-500);
            line-height: 1.6;
            font-weight: 500;
            font-family: 'Lora', serif;
          }
        }
      }
      
      .edit-form {
        .form-section {
          margin-bottom: 32px;
          
          .section-title {
            font-size: 18px;
            font-weight: 700;
            color: var(--newsprint-fg);
            margin: 0 0 20px 0;
            padding-bottom: 12px;
            border-bottom: 1px solid var(--newsprint-border);
            position: relative;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            
            &::before {
              content: '';
              position: absolute;
              bottom: -1px;
              left: 0;
              width: 40px;
              height: 2px;
              background: var(--newsprint-accent);
            }
          }
          
          .form-row {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 24px;
            margin-bottom: 20px;
            
            &:last-child {
              margin-bottom: 0;
            }
            
            .el-form-item {
              margin-bottom: 0;
            }
          }
          
          .form-input,
          .form-select {
            .el-input__wrapper {
              background: var(--newsprint-bg);
              border: 1px solid var(--newsprint-border);
              padding: 16px 20px;
              transition: all 0.2s ease;
              position: relative;
              overflow: hidden;
              
              &:hover {
                border-color: var(--newsprint-fg);
              }
              
              &.is-focus {
                border-color: var(--newsprint-fg);
                box-shadow: 2px 2px 0px 0px var(--newsprint-fg);
                transform: translate(-1px, -1px);
              }
            }
            
            .el-input__inner {
              font-size: 15px;
              color: var(--newsprint-fg);
              font-weight: 500;
              font-family: 'Lora', serif;
              
              &::placeholder {
                color: var(--newsprint-neutral-400);
                font-weight: 400;
              }
            }
            
            .el-input__count {
              color: var(--newsprint-neutral-500);
              font-weight: 500;
              font-size: 13px;
            }
          }
          
          .el-form-item__label {
            font-weight: 700;
            color: var(--newsprint-fg);
            font-size: 15px;
            position: relative;
            
            &::before {
              content: '*';
              color: var(--newsprint-accent);
              margin-right: 4px;
              font-weight: 800;
            }
          }
        }
        
        .form-actions {
          display: flex;
          justify-content: center;
          align-items: center;
          gap: 20px;
          margin-top: 40px;
          padding-top: 32px;
          border-top: 2px solid var(--newsprint-border);
          
          .action-btn {
            padding: 16px 32px;
            font-weight: 700;
            font-size: 15px;
            transition: all 0.2s ease;
            border: 1px solid var(--newsprint-border);
            min-width: 140px;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            
            &:hover {
              transform: translate(-2px, -2px);
            }
            
            &:active {
              transform: translate(0, 0);
            }
            
            &.cancel-btn {
              background: var(--newsprint-bg);
              border-color: var(--newsprint-border);
              color: var(--newsprint-neutral-500);
              
              &:hover {
                border-color: var(--newsprint-fg);
                color: var(--newsprint-fg);
                box-shadow: 2px 2px 0px 0px var(--newsprint-fg);
              }
            }
            
            &.primary-btn {
              background: var(--newsprint-fg);
              border-color: var(--newsprint-fg);
              color: var(--newsprint-bg);
              
              &:hover {
                background: var(--newsprint-bg);
                color: var(--newsprint-fg);
                box-shadow: 4px 4px 0px 0px var(--newsprint-fg);
              }
            }
          }
        }
      }
    }
  }
  
  .empty-state {
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: center;
    height: 100%;
    text-align: center;
    background: var(--newsprint-bg);
    padding: 80px 40px;
    box-shadow: 4px 4px 0px 0px var(--newsprint-border);
    border: 1px solid var(--newsprint-border);
    
    .empty-icon {
      font-size: 80px;
      color: var(--newsprint-neutral-400);
      margin-bottom: 24px;
    }
    
    h3 {
      margin: 0 0 12px 0;
      font-size: 24px;
      font-weight: 700;
      color: var(--newsprint-fg);
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    
    p {
      margin: 0 0 32px 0;
      color: var(--newsprint-neutral-500);
      font-size: 16px;
      font-family: 'Lora', serif;
    }
    
    .el-button--primary {
      background: var(--newsprint-fg) !important;
      color: var(--newsprint-bg) !important;
      border: 2px solid var(--newsprint-fg) !important;
      
      &:hover {
        background: var(--newsprint-bg) !important;
        color: var(--newsprint-fg) !important;
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .model-editor-page {
    padding: 16px;
    
         .page-header {
       flex-direction: column;
       gap: 20px;
       padding: 20px;
       
       .header-left {
         justify-content: center;
         
         .breadcrumb {
           font-size: 14px;
           
           .breadcrumb-item {
             padding: 6px 10px;
           }
         }
       }
     }
    
    .edit-form-section .form-container {
      padding: 24px;
      
      .form-header {
        flex-direction: column;
        text-align: center;
        gap: 16px;
      }
      
      .edit-form .form-section .form-row {
        grid-template-columns: 1fr;
        gap: 16px;
      }
      
             .edit-form .form-actions {
         flex-direction: column;
         gap: 16px;
         
         .action-btn {
           width: 100%;
           max-width: 200px;
         }
       }
    }
  }
}
</style> 