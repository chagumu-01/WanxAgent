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
  background: linear-gradient(135deg, #fceef2 0%, #f8d0d8 50%, #f2a5b5 100%);
  position: relative;
  overflow: hidden;
  font-family: 'PingFang SC', 'Helvetica Neue', Arial, sans-serif;
}

.bg-decoration {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1;

  .blob {
    position: absolute;
    filter: blur(80px);
    border-radius: 50%;
    opacity: 0.5;
    z-index: 1;
  }

  .blob-1 {
    width: 400px;
    height: 400px;
    background: #f2a5b5;
    top: -100px;
    right: -100px;
    animation: move1 20s infinite alternate;
  }

  .blob-2 {
    width: 500px;
    height: 500px;
    background: #e87187;
    bottom: -150px;
    left: -100px;
    animation: move2 25s infinite alternate;
  }

  .blob-3 {
    width: 300px;
    height: 300px;
    background: #f8d0d8;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
  }
}

@keyframes move1 {
  from { transform: translate(0, 0); }
  to { transform: translate(-100px, 100px); }
}

@keyframes move2 {
  from { transform: translate(0, 0); }
  to { transform: translate(150px, -100px); }
}

.login-card {
  width: 100%;
  max-width: 440px;
  background: rgba(255, 255, 255, 0.9);
  backdrop-filter: blur(20px);
  border: 1px solid rgba(242, 165, 181, 0.5);
  border-radius: 24px;
  padding: 40px;
  box-shadow: 0 20px 40px rgba(196, 30, 58, 0.1);
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
      background: #ffffff;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 3px solid #c41e3a;
      box-shadow: 0 8px 16px rgba(196, 30, 58, 0.3);
      
      .logo-svg {
        width: 44px;
        height: 44px;
      }
    }

    .logo-text {
      font-size: 28px;
      font-weight: 800;
      color: #c41e3a;
      margin: 0;
      letter-spacing: 1px;
    }
  }

  .subtitle {
    font-size: 15px;
    color: #c41e3a;
    margin: 0;
  }
}

.login-form {
  .form-item {
    margin-bottom: 20px;
  }

  .custom-input {
    :deep(.el-input__wrapper) {
      background-color: #fff;
      border: 1px solid #f2a5b5;
      box-shadow: none !important;
      border-radius: 12px;
      padding: 4px 12px;
      transition: all 0.3s ease;

      &:hover {
        border-color: #c41e3a;
      }

      &.is-focus {
        border-color: #c41e3a;
        background-color: #fff;
        box-shadow: 0 0 0 4px rgba(196, 30, 58, 0.1) !important;
      }
    }

    :deep(.el-input__inner) {
      height: 48px;
      font-size: 15px;
      color: #4a1a25;

      &::placeholder {
        color: #d94560;
      }
    }

    :deep(.el-input__prefix-inner) {
      color: #c41e3a;
      font-size: 18px;
    }
  }

  .form-options {
    display: flex;
    justify-content: space-between;
    align-items: center;
    margin-bottom: 30px;

    :deep(.el-checkbox__label) {
      color: #c41e3a;
      font-size: 14px;
    }

    :deep(.el-checkbox__input.is-checked .el-checkbox__inner) {
      background-color: #c41e3a;
      border-color: #c41e3a;
    }

    .forgot-pwd {
      font-size: 14px;
      color: #c41e3a;
      text-decoration: none;
      transition: color 0.3s;

      &:hover {
        color: #9e1830;
      }
    }
  }

  .login-btn {
    width: 100%;
    height: 52px;
    border-radius: 12px;
    background: linear-gradient(135deg, #c41e3a 0%, #d94560 100%);
    border: none;
    font-size: 16px;
    font-weight: 600;
    color: #fff;
    margin-bottom: 20px;
    transition: all 0.3s ease;

    &:hover {
      transform: translateY(-2px);
      box-shadow: 0 10px 20px rgba(196, 30, 58, 0.3);
      opacity: 0.95;
    }

    &:active {
      transform: translateY(0);
    }
  }

  .register-footer {
    text-align: center;
    font-size: 14px;
    color: #c41e3a;

    :deep(.el-button--link) {
      color: #c41e3a;
      font-weight: 600;
      padding: 0 4px;
      
      &:hover {
        color: #9e1830;
      }
    }
  }
}

.footer {
  margin-top: 40px;
  padding-top: 20px;
  border-top: 1px solid #f2a5b5;
  display: flex;
  justify-content: space-between;
  align-items: center;

  .version {
    font-size: 12px;
    color: #d94560;
    background: #fceef2;
    padding: 2px 8px;
    border-radius: 6px;
  }
}
</style>