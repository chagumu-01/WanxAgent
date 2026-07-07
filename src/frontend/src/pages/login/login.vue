<template>
  <div class="login-container">
    <div class="bg-decoration">
      <div class="blob blob-1"></div>
      <div class="blob blob-2"></div>
      <div class="blob blob-3"></div>
    </div>

    <div class="login-card">
      <div class="login-card-inner">
        <div class="header">
          <div class="logo-wrapper">
            <div class="logo-icon">
              <svg viewBox="0 0 100 100" class="logo-svg">
                <path d="M50 15 C30 15 15 30 15 50 C15 70 30 85 50 85 C70 85 85 70 85 50 C85 30 70 15 50 15 Z" 
                      fill="none" stroke="#c41e3a" stroke-width="8"/>
                <path d="M30 50 C30 50 45 30 50 35 C55 30 70 50 70 50" 
                      fill="none" stroke="#c41e3a" stroke-width="8" stroke-linecap="round"/>
                <path d="M30 50 C30 50 45 70 50 65 C55 70 70 50 70 50" 
                      fill="none" stroke="#c41e3a" stroke-width="8" stroke-linecap="round"/>
              </svg>
            </div>
            <h1 class="logo-text">WanxAgent</h1>
          </div>
          <p class="subtitle">开启您的智能协作新纪元</p>
        </div>

        <div class="login-form">
          <div class="form-item">
            <div class="input-wrapper">
              <el-input
                v-model="loginForm.username"
                placeholder="用户名 / 账号"
                size="large"
                class="custom-input"
                @keyup.enter="handleLogin"
              >
                <template #prefix>
                  <el-icon><UserIcon /></el-icon>
                </template>
              </el-input>
            </div>
          </div>

          <div class="form-item">
            <div class="input-wrapper">
              <el-input
                v-model="loginForm.password"
                type="password"
                placeholder="密码"
                size="large"
                class="custom-input"
                show-password
                @keyup.enter="handleLogin"
              >
                <template #prefix>
                  <el-icon><LockIcon /></el-icon>
                </template>
              </el-input>
            </div>
          </div>

          <div class="form-options">
            <el-checkbox v-model="rememberMe">记住我</el-checkbox>
            <a href="#" class="forgot-pwd">忘记密码？</a>
          </div>

          <el-button
            type="primary"
            class="login-btn"
            :loading="loading"
            @click="handleLogin"
          >
            进入平台
          </el-button>

          <div class="register-footer">
            <span>还没有账号？</span>
            <el-button link type="primary" @click="goToRegister">立即注册</el-button>
          </div>
        </div>

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
import { User as UserIcon, Lock as LockIcon } from 'lucide-vue-next'
import { loginAPI, getUserInfoAPI } from '../../apis/auth'
import { useUserStore } from '../../store/user'

const router = useRouter()
const userStore = useUserStore()

const loginForm = reactive({
  username: '',
  password: ''
})

const loading = ref(false)
const rememberMe = ref(false)

const handleLogin = async () => {
  if (!loginForm.username || !loginForm.password) {
    ElMessage.warning('请输入用户名和密码')
    return
  }

  try {
    loading.value = true
    const response = await loginAPI(loginForm)
    const responseData = response.data
    if (responseData.status_code === 200) {
      ElMessage.success('登录成功')
      const userData = responseData.data || {}
      if (userData.access_token && userData.user_id) {
        userStore.setUserInfo(userData.access_token, {
          id: userData.user_id,
          username: loginForm.username
        })
        try {
          const userInfoResponse = await getUserInfoAPI(userData.user_id)
          const userInfoData = userInfoResponse.data
          if (userInfoData.status_code === 200) {
            const completeUserData = userInfoData.data || {}
            userStore.updateUserInfo({
              avatar: completeUserData.user_avatar || completeUserData.avatar,
              description: completeUserData.user_description || completeUserData.description
            })
          }
        } catch (error) {
          console.error('获取用户详细信息失败:', error)
        }
      }
      router.push('/')
    } else {
      ElMessage.error(responseData.status_message || '登录失败')
    }
  } catch (error: any) {
    console.error('登录错误:', error)
    if (error.response?.data?.message) {
      ElMessage.error(error.response.data.status_message)
    } else if (error.response?.data?.detail) {
      ElMessage.error(error.response.data.detail)
    } else {
      ElMessage.error('登录失败，请检查网络连接')
    }
  } finally {
    loading.value = false
  }
}

const goToRegister = () => {
  router.push('/register')
}
</script>

<style lang="scss" scoped>
.login-container {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--newsprint-bg);
  position: relative;
  overflow: hidden;
}

.login-card {
  width: 100%;
  max-width: 440px;
  background: var(--newsprint-bg);
  border: 1px solid var(--newsprint-border);
  box-shadow: 8px 8px 0px 0px var(--newsprint-fg);
  padding: 40px;
  position: relative;
  z-index: 2;
  margin: 20px;
}

.header {
  text-align: center;
  margin-bottom: 40px;

  .logo-wrapper {
    display: flex;
    flex-direction: column;
    align-items: center;
    gap: 12px;
    margin-bottom: 16px;

    .logo-icon {
      width: 64px;
      height: 64px;
      background: var(--newsprint-fg);
      display: flex;
      align-items: center;
      justify-content: center;
      border: 3px solid var(--newsprint-fg);
      
      .logo-svg {
        width: 44px;
        height: 44px;
        
        path {
          stroke: var(--newsprint-bg) !important;
        }
      }
    }

    .logo-text {
      font-size: 28px;
      font-weight: 800;
      color: var(--newsprint-fg);
      margin: 0;
      letter-spacing: 1px;
      font-family: 'Playfair Display', serif;
      text-transform: uppercase;
      letter-spacing: 0.1em;
    }
  }

  .subtitle {
    font-size: 15px;
    color: var(--newsprint-neutral-500);
    margin: 0;
    font-family: 'Lora', serif;
  }
}

.login-form {
  .form-item {
    margin-bottom: 20px;
  }

  .custom-input {
    :deep(.el-input__wrapper) {
      background-color: var(--newsprint-bg);
      border: 1px solid var(--newsprint-border);
      box-shadow: none !important;
      padding: 4px 12px;
      transition: all 0.2s ease;

      &:hover {
        border-color: var(--newsprint-fg);
      }

      &.is-focus {
        border-color: var(--newsprint-fg);
        background-color: var(--newsprint-bg);
        box-shadow: 2px 2px 0px 0px var(--newsprint-fg) !important;
        transform: translate(-1px, -1px);
      }
    }

    :deep(.el-input__inner) {
      height: 48px;
      font-size: 15px;
      color: var(--newsprint-fg);
      font-family: 'Lora', serif;

      &::placeholder {
        color: var(--newsprint-neutral-400);
      }
    }

    :deep(.el-input__prefix-inner) {
      color: var(--newsprint-fg);
      font-size: 18px;
    }
  }

  .form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;

    :deep(.el-checkbox__label) {
      color: var(--newsprint-neutral-500);
      font-size: 14px;
      font-family: 'Lora', serif;
    }

    :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
      background-color: var(--newsprint-fg);
      border-color: var(--newsprint-fg);
    }

    :deep(.el-checkbox__inner) {
      border-color: var(--newsprint-border);
    }

    .forgot-pwd {
      font-size: 14px;
      color: var(--newsprint-neutral-500);
      text-decoration: none;
      transition: color 0.2s;

      &:hover {
        color: var(--newsprint-fg);
      }
    }
  }

  .login-btn {
    width: 100%;
    height: 52px;
    background: var(--newsprint-fg);
    border: 2px solid var(--newsprint-fg);
    font-size: 16px;
    font-weight: 600;
    color: var(--newsprint-bg);
    margin-bottom: 20px;
    transition: all 0.2s ease;
    text-transform: uppercase;
    letter-spacing: 0.1em;

    &:hover {
      transform: translate(-2px, -2px);
      box-shadow: 4px 4px 0px 0px var(--newsprint-fg);
      background: var(--newsprint-bg);
      color: var(--newsprint-fg);
    }

    &:active {
      transform: translate(0, 0);
    }
  }

  .register-footer {
    text-align: center;
    font-size: 14px;
    color: var(--newsprint-neutral-500);

    :deep(.el-button--link) {
      color: var(--newsprint-fg);
      font-weight: 600;
      padding: 0 4px;
      
      &:hover {
        color: var(--newsprint-accent);
      }
    }
  }
}

.footer {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid var(--newsprint-border);
  display: flex;
  justify-content: space-between;
  align-items: center;

  .version {
    font-size: 12px;
    color: var(--newsprint-neutral-500);
    background: var(--newsprint-neutral-100);
    padding: 2px 8px;
    border: 1px solid var(--newsprint-border);
    text-transform: uppercase;
    letter-spacing: 0.05em;
  }
}
</style>