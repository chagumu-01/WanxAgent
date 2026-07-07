<template>
  <div class="register-container">
    <!-- 背景装饰元素 -->
    <div class="bg-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <!-- 注册卡片 -->
    <div class="register-card">
      <div class="register-card-inner">
        <!-- Logo和标题 -->
        <div class="header">
          <div class="logo-wrapper">
            <div class="logo-icon">
              <img src="../../assets/agentchat.svg" alt="WanxAgent" class="logo-img" />
            </div>
            <h1 class="logo-text">WanxAgent</h1>
          </div>
          <p class="subtitle">创建您的账户，开启智能协作之旅</p>
        </div>

        <!-- 注册表单 -->
        <div class="register-form">
          <div class="form-item">
            <el-input
              v-model="registerForm.user_name"
              placeholder="用户名"
              size="large"
              class="custom-input"
              @keyup.enter="handleRegister"
            >
              <template #prefix>
                <el-icon><User /></el-icon>
              </template>
            </el-input>
          </div>

          <div class="form-item">
            <el-input
              v-model="registerForm.user_email"
              placeholder="邮箱地址 (可选)"
              size="large"
              class="custom-input"
              @keyup.enter="handleRegister"
            >
              <template #prefix>
                <el-icon><Message /></el-icon>
              </template>
            </el-input>
          </div>

          <div class="form-item">
            <el-input
              v-model="registerForm.user_password"
              type="password"
              placeholder="设置密码"
              size="large"
              class="custom-input"
              show-password
              @keyup.enter="handleRegister"
            >
              <template #prefix>
                <el-icon><Lock /></el-icon>
              </template>
            </el-input>
          </div>

          <div class="form-item">
            <el-input
              v-model="confirmPassword"
              type="password"
              placeholder="确认密码"
              size="large"
              class="custom-input"
              show-password
              @keyup.enter="handleRegister"
            >
              <template #prefix>
                <el-icon><Checked /></el-icon>
              </template>
            </el-input>
          </div>

          <el-button
            type="primary"
            class="register-btn"
            :loading="loading"
            @click="handleRegister"
          >
            立即注册
          </el-button>

          <div class="login-footer">
            <span>已有账号？</span>
            <el-button link type="primary" @click="goToLogin">去登录</el-button>
          </div>
        </div>

        <!-- 底部版本信息 -->
        <div class="footer">
          <span class="version">v2.4.0</span>
          
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, reactive } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { User, Lock, Message, Checked } from '@element-plus/icons-vue'
import { registerAPI } from '../../apis/auth'
import type { RegisterForm } from '../../apis/auth'

const router = useRouter()

const registerForm = reactive<RegisterForm>({
  user_name: '',
  user_email: '',
  user_password: ''
})

const confirmPassword = ref('')
const loading = ref(false)

const validateForm = () => {
  if (!registerForm.user_name) {
    ElMessage.warning('请输入用户名')
    return false
  }
  
  if (registerForm.user_name.length > 20) {
    ElMessage.warning('用户名长度不应该超过20个字符')
    return false
  }
  
  if (!registerForm.user_password) {
    ElMessage.warning('请输入密码')
    return false
  }
  
  if (registerForm.user_password.length < 6) {
    ElMessage.warning('密码长度至少6个字符')
    return false
  }
  
  if (registerForm.user_password !== confirmPassword.value) {
    ElMessage.warning('两次输入的密码不一致')
    return false
  }
  
  if (registerForm.user_email && !/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(registerForm.user_email)) {
    ElMessage.warning('请输入有效的邮箱地址')
    return false
  }
  
  return true
}

const handleRegister = async () => {
  if (!validateForm()) {
    return
  }

  try {
    loading.value = true
    const response = await registerAPI(registerForm)
    
    if (response.data.status_code === 200) {
      ElMessage.success('注册成功，请登录')
      router.push('/login')
    } else {
      ElMessage.error(response.data.status_message || '注册失败')
    }
  } catch (error: any) {
    console.error('注册错误:', error)
    if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('注册失败，请检查网络连接')
    }
  } finally {
    loading.value = false
  }
}

const goToLogin = () => {
  router.push('/login')
}
</script>

<style lang="scss" scoped>
.register-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--newsprint-bg);
  position: relative;
  overflow: hidden;
  font-family: 'Inter', 'Helvetica Neue', sans-serif;
}

.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='4' height='4' viewBox='0 0 4 4'%3E%3Cpath fill='%23111111' fill-opacity='0.04' d='M1 3h1v1H1V3zm2-2h1v1H3V1z'%3E%3C/path%3E%3C/svg%3E");
}

.register-card {
  width: 100%;
  max-width: 440px;
  background: var(--newsprint-bg);
  border: 2px solid var(--newsprint-border);
  padding: 40px;
  position: relative;
  z-index: 2;
  margin: 20px;
  box-shadow: 4px 4px 0px 0px var(--newsprint-border);

  &:hover {
    box-shadow: 6px 6px 0px 0px var(--newsprint-border);
    transform: translate(-2px, -2px);
    transition: all 0.2s ease-out;
  }
}

.header {
  text-align: center;
  margin-bottom: 30px;

  .logo-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    margin-bottom: 12px;

    .logo-icon {
      width: 56px;
      height: 56px;
      background: var(--newsprint-bg);
      border: 2px solid var(--newsprint-border);
      display: flex;
      align-items: center;
      justify-content: center;
      
      .logo-img {
        width: 32px;
        height: 32px;
      }
    }

    .logo-text {
      font-size: 26px;
      font-weight: 900;
      color: var(--newsprint-fg);
      margin: 0;
      letter-spacing: 2px;
      font-family: 'Playfair Display', serif;
    }
  }

  .subtitle {
    font-size: 14px;
    color: var(--newsprint-neutral-500);
    margin: 0;
    font-family: 'Lora', serif;
  }
}

.register-form {
  .form-item {
    margin-bottom: 20px;
  }

  .custom-input {
    :deep(.el-input__wrapper) {
      background-color: transparent;
      border: none !important;
      border-bottom: 2px solid var(--newsprint-border) !important;
      box-shadow: none !important;
      padding: 4px 0;
      transition: all 0.2s ease;

      &:hover {
        border-bottom-color: var(--newsprint-accent);
      }

      &.is-focus {
        border-bottom-color: var(--newsprint-accent);
        background-color: #F0F0F0;
      }
    }

    :deep(.el-input__inner) {
      height: 44px;
      font-size: 14px;
      color: var(--newsprint-fg);
      font-family: 'JetBrains Mono', monospace;

      &::placeholder {
        color: var(--newsprint-neutral-400);
      }
    }

    :deep(.el-input__prefix-inner) {
      color: var(--newsprint-fg);
      font-size: 18px;
    }
  }

  .register-btn {
    width: 100%;
    height: 48px;
    background: var(--newsprint-fg);
    border: 2px solid var(--newsprint-fg);
    font-size: 14px;
    font-weight: 600;
    color: var(--newsprint-bg);
    margin-top: 10px;
    margin-bottom: 16px;
    transition: all 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.1em;

    &:hover {
      background: var(--newsprint-bg);
      color: var(--newsprint-fg);
      border-color: var(--newsprint-fg);
      box-shadow: 4px 4px 0px 0px var(--newsprint-fg);
      transform: translate(-2px, -2px);
    }

    &:active {
      transform: translate(0, 0);
      box-shadow: 0 0 0 0 var(--newsprint-fg);
    }
  }

  .login-footer {
    text-align: center;
    font-size: 14px;
    color: var(--newsprint-neutral-500);

    :deep(.el-button--link) {
      color: var(--newsprint-accent);
      font-weight: 600;
      padding: 0 4px;
      
      &:hover {
        color: var(--newsprint-fg);
      }
    }
  }
}

.footer {
  margin-top: 30px;
  padding-top: 16px;
  border-top: 1px solid var(--newsprint-border);
  display: flex;
  justify-content: space-between;
  align-items: center;

  .version {
    font-size: 11px;
    color: var(--newsprint-neutral-500);
    background: var(--newsprint-neutral-100);
    padding: 2px 6px;
    border: 1px solid var(--newsprint-border);
    font-family: 'JetBrains Mono', monospace;
  }
}
</style>
 