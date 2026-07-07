<script setup lang="ts">
import { ref, onMounted } from "vue"
import { getDialogListAPI } from "../../../apis/history"

const shouldShow = ref(false)

onMounted(async () => {
  try {
    const response = await getDialogListAPI()
    if (response.data.status_code === 200 && response.data.data && response.data.data.length > 0) {
      return
    }
  } catch (_) {
    // ignore
  }
  shouldShow.value = true
})
</script>

<template>
  <!-- 对话列表为空时，右侧展示空白 -->
  <div v-if="shouldShow"></div>
  <!-- 如果有会话记录，不显示任何内容，等待跳转 -->
</template>

<style lang="scss" scoped>
.default-page {
  display: flex;
  flex-direction: column;
  height: 100%;
  padding: 24px;
  background-color: var(--newsprint-bg);
  min-height: 100vh;

  .header-section {
    text-align: center;
    margin-bottom: 40px;

    .welcome-content {
      display: flex;
      flex-direction: column;
      align-items: center;
      gap: 20px;

      .welcome-icon {
        background: var(--newsprint-neutral-100);
        border: 2px solid var(--newsprint-border);
        padding: 20px;
      }

      .welcome-text {
        .title {
          font-size: 2.5rem;
          font-weight: 700;
          color: var(--newsprint-fg);
          margin: 0 0 12px 0;
          font-family: 'Playfair Display', serif;

          .highlight {
            color: var(--newsprint-accent);
          }
        }

        .subtitle {
          font-size: 1.1rem;
          color: var(--newsprint-neutral-500);
          margin: 0;
          font-weight: 400;
          font-family: 'Lora', serif;
        }
      }
    }
  }

  .search-section {
    margin-bottom: 40px;

    .search-container {
      max-width: 600px;
      margin: 0 auto;

      .search-input {
        :deep(.el-input__wrapper) {
          background-color: transparent;
          border: none !important;
          border-bottom: 2px solid var(--newsprint-border) !important;
          box-shadow: none !important;
          padding: 4px 0;
          
          &:hover {
            border-bottom-color: var(--newsprint-accent);
          }
          
          &.is-focus {
            border-bottom-color: var(--newsprint-accent);
            background: #F0F0F0;
          }
        }

        :deep(.el-input-group__append) {
          .el-button {
            border: 2px solid var(--newsprint-fg);
            background: var(--newsprint-fg);
            color: var(--newsprint-bg);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            
            &:hover {
              background: var(--newsprint-bg);
              color: var(--newsprint-fg);
              box-shadow: 4px 4px 0px 0px var(--newsprint-fg);
              transform: translate(-2px, -2px);
            }
          }
        }
      }
    }
  }

  .agents-section {
    flex: 1;
    background: var(--newsprint-bg);
    border: 2px solid var(--newsprint-border);
    padding: 32px;
    box-shadow: 4px 4px 0px 0px var(--newsprint-border);

    .section-header {
      display: flex;
      justify-content: space-between;
      align-items: center;
      margin-bottom: 24px;

      .header-left {
        display: flex;
        align-items: center;
        gap: 8px;

        .section-title {
          font-size: 1.5rem;
          font-weight: 600;
          color: var(--newsprint-fg);
          margin: 0;
          text-transform: uppercase;
          letter-spacing: 0.05em;
        }

        .agent-count {
          font-size: 0.9rem;
          color: var(--newsprint-neutral-500);
          background: var(--newsprint-neutral-100);
          padding: 4px 8px;
          border: 1px solid var(--newsprint-border);
          font-family: 'JetBrains Mono', monospace;
        }
      }
    }

    .loading-state {
      padding: 40px 0;
    }

    .empty-state {
      text-align: center;
      padding: 60px 20px;
      color: var(--newsprint-neutral-500);

      .empty-icon {
        font-size: 4rem;
        margin-bottom: 16px;
      }

      .empty-title {
        font-size: 1.25rem;
        font-weight: 600;
        margin-bottom: 8px;
        color: var(--newsprint-fg);
        font-family: 'Playfair Display', serif;
      }

      .empty-description {
        font-size: 0.9rem;
        margin-bottom: 24px;
        color: var(--newsprint-neutral-500);
      }
    }

    .agents-grid {
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
      gap: 24px;

      .agent-item {
        .agent-card {
          transition: all 0.2s ease;
          border: 1px solid var(--newsprint-border);
          overflow: hidden;

          &:hover {
            transform: translate(-2px, -2px);
            box-shadow: 4px 4px 0px 0px var(--newsprint-border);
          }
        }
      }
    }
  }
}

// 响应式设计
@media (max-width: 768px) {
  .default-page {
    padding: 16px;

    .header-section {
      .welcome-content {
        .welcome-text {
          .title {
            font-size: 2rem;
          }

          .subtitle {
            font-size: 1rem;
          }
        }
      }
    }

    .agents-section {
      padding: 20px;

      .section-header {
        flex-direction: column;
        gap: 16px;
        align-items: flex-start;
      }

      .agents-grid {
        grid-template-columns: 1fr;
        gap: 16px;
      }
    }
  }
}

@media (max-width: 480px) {
  .default-page {
    .header-section {
      .welcome-content {
        .welcome-text {
          .title {
            font-size: 1.5rem;
          }
        }
      }
    }
  }
}
</style>
