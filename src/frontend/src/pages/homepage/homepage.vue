<script setup lang="ts">
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { 
  ArrowRight, 
  Bot, 
  Search, 
  Newspaper, 
  PieChart,
  Zap,
  FileText
} from 'lucide-vue-next'

const router = useRouter()
const searchQuery = ref('')

const isMac = computed(() => {
  return typeof navigator !== 'undefined' && navigator.platform.toUpperCase().indexOf('MAC') >= 0
})

const examples = [
  {
    title: '自动构建智能体',
    category: '自动模式',
    description: '使用多个工具相互配合完成自动构建智能体的任务',
    action: '开始构建 →',
    icon: Bot,
    iconColor: 'var(--newsprint-accent)'
  },
  {
    title: '深度搜索',
    category: '搜索模式',
    description: '连接外部互联网资源，扩展系统能力和数据源',
    action: '开始搜索 →',
    icon: Search,
    iconColor: 'var(--newsprint-accent)'
  },
  {
    title: 'AI日报',
    category: '生成模式',
    description: '对最近的AI新闻进行整理总结，可生成下载链接',
    action: '生成日报 →',
    icon: Newspaper,
    iconColor: 'var(--newsprint-accent)'
  },
  {
    title: '知识库问答',
    category: '知识库模式',
    description: '基于已有知识库进行精准问答和信息检索',
    action: '查询知识 →',
    icon: FileText,
    iconColor: 'var(--newsprint-accent)'
  }
]

const handleSearch = async () => {
  if (searchQuery.value.trim()) {
    router.push({
      path: '/mars',
      query: {
        message: searchQuery.value
      }
    })
  }
}

const handleKeydown = (event: KeyboardEvent) => {
  if ((event.metaKey || event.ctrlKey) && event.key === 'Enter') {
    event.preventDefault()
    handleSearch()
  }
}

const handleExampleClick = async (example: any, index: number) => {
  const example_id = index + 1
  
  router.push({
    path: '/mars',
    query: {
      example_id: example_id
    }
  })
}
</script>

<template>
  <div class="homepage">
    <div class="logo-section">
      <div class="logo-container">
        <div class="logo-icon">
          <svg viewBox="0 0 100 100" class="logo-svg">
            <path d="M50 15 C30 15 15 30 15 50 C15 70 30 85 50 85 C70 85 85 70 85 50 C85 30 70 15 50 15 Z" 
                  fill="none" stroke="var(--newsprint-accent)" stroke-width="8"/>
            <path d="M30 50 C30 50 45 30 50 35 C55 30 70 50 70 50" 
                  fill="none" stroke="var(--newsprint-accent)" stroke-width="8" stroke-linecap="round"/>
            <path d="M30 50 C30 50 45 70 50 65 C55 70 70 50 70 50" 
                  fill="none" stroke="var(--newsprint-accent)" stroke-width="8" stroke-linecap="round"/>
          </svg>
        </div>
        <h1 class="brand-name">WanxAgent</h1>
      </div>
      <p class="brand-slogan">智能协作，无限可能</p>
    </div>

    <div class="search-section">
      <div class="search-container">
        <div class="search-box">
          <div class="search-input-wrapper">
            <textarea
              v-model="searchQuery"
              placeholder="WanxAgent会完成你的任务并输出结果。"
              class="search-input"
              @keydown="handleKeydown"
              rows="3"
            ></textarea>
            
            <div class="search-controls">
              <div class="search-send-container">
                <span class="shortcut-hint">{{ isMac ? '⌘+↵' : 'Ctrl + ↵ ' }}发送</span>
                <button class="send-button" @click="handleSearch">
                  <ArrowRight :size="18" />
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div class="examples-section">
      <h2 class="section-title">
        优秀案例
        <span class="section-subtitle"></span>
      </h2>

      <div class="examples-grid">
        <div
          v-for="(example, index) in examples"
          :key="index"
          class="example-card"
          @click="handleExampleClick(example, index)"
        >
          <div class="example-header">
            <div class="example-icon" :style="{ background: `linear-gradient(135deg, ${example.iconColor}, ${adjustColor(example.iconColor, 30)})` }">
              <component :is="example.icon" :size="20" />
            </div>
            <div class="example-title-wrapper">
              <h3 class="example-title">{{ example.title }}</h3>
              <span class="example-category">{{ example.category }}</span>
            </div>
          </div>
          <p class="example-description">{{ example.description }}</p>
          <div class="example-action">
            {{ example.action }}
            <ArrowRight :size="14" />
          </div>
          
          <div class="example-preview">
            <div v-if="index === 0" class="robot-preview">
              <div class="assembly-icon">
                <Zap :size="16" />
              </div>
              <div class="assembly-tools">
                <div class="tool-box"></div>
                <div class="connector"></div>
                <div class="component"></div>
              </div>
            </div>
            <div v-else-if="index === 1" class="search-preview">
              <div class="search-container">
                <div class="search-box-icon">
                  <Search :size="10" />
                </div>
                <div class="search-box"></div>
              </div>
              <div class="search-waves">
                <div class="wave wave1"></div>
                <div class="wave wave2"></div>
                <div class="wave wave3"></div>
              </div>
            </div>
            <div v-else-if="index === 2" class="news-preview">
              <div class="news-header">
                <div class="news-title"></div>
                <div class="news-date"></div>
              </div>
              <div class="news-content">
                <div class="news-line long"></div>
                <div class="news-line medium"></div>
                <div class="news-line short"></div>
                <div class="news-line medium"></div>
              </div>
              <div class="news-badge">AI</div>
            </div>
            <div v-else class="pie-preview">
              <div class="pie-chart">
                <div class="pie-slice slice1"></div>
                <div class="pie-slice slice2"></div>
                <div class="pie-slice slice3"></div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
const adjustColor = (hex: string, percent: number): string => {
  const num = parseInt(hex.replace('#', ''), 16)
  const amt = Math.round(2.55 * percent)
  const R = (num >> 16) + amt
  const G = (num >> 8 & 0x00FF) + amt
  const B = (num & 0x0000FF) + amt
  return '#' + (0x1000000 +
    (R < 255 ? (R < 1 ? 0 : R) : 255) * 0x10000 +
    (G < 255 ? (G < 1 ? 0 : G) : 255) * 0x100 +
    (B < 255 ? (B < 1 ? 0 : B) : 255)).toString(16).slice(1)
}

export default {
  methods: {
    adjustColor
  }
}
</script>

<style lang="scss" scoped>
.homepage {
  min-height: 100vh;
  background: var(--newsprint-bg);
  padding: 10px 15px;
  overflow-y: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  &::-webkit-scrollbar { display: none; }
}

.logo-section {
  text-align: center;
  margin-bottom: 30px;
  
  .logo-container {
    display: inline-flex;
    align-items: center;
    gap: 16px;
    
    .logo-icon {
      width: 56px;
      height: 56px;
      background: var(--newsprint-bg);
      display: flex;
      align-items: center;
      justify-content: center;
      border: 3px solid var(--newsprint-accent);
      box-shadow: 4px 4px 0px 0px var(--newsprint-fg);
      animation: float 3s ease-in-out infinite;
      
      .logo-svg {
        width: 40px;
        height: 40px;
      }
    }
    
    .brand-name {
      font-size: 48px;
      font-weight: 800;
      color: var(--newsprint-fg);
      margin: 0;
      position: relative;
      letter-spacing: -1px;
      font-family: 'Playfair Display', serif;
      
      &::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 0;
        right: 0;
        height: 3px;
        background: var(--newsprint-accent);
        opacity: 0.8;
      }
    }
  }
  
  .brand-slogan {
    font-size: 14px;
    color: var(--newsprint-fg-muted);
    margin-top: 12px;
    font-weight: 400;
    letter-spacing: 0.1em;
    text-transform: uppercase;
  }
}

@keyframes float {
  0%, 100% { transform: translateY(0px); }
  50% { transform: translateY(-8px); }
}

.search-section {
  max-width: 750px;
  margin: 0 auto 28px;
  
  .search-container {
    background: var(--newsprint-neutral-100);
    padding: 32px;
    box-shadow: 4px 4px 0px 0px var(--newsprint-fg);
    border: 2px solid var(--newsprint-fg);
  }
  
  .search-box {
    margin-bottom: 18px;
    
    .search-input-wrapper {
      background: var(--newsprint-bg);
      padding: 14px;
      border: 2px solid var(--newsprint-fg);
      transition: all 0.3s ease;
      min-height: 160px;
      width: 100%;
      display: block;
      position: relative;
      
      &:focus-within {
        box-shadow: 4px 4px 0px 0px var(--newsprint-accent);
      }
      
      .search-input {
        width: 100%;
        border: none;
        background: transparent;
        padding: 12px 18px 45px 18px;
        font-size: 19px;
        outline: none;
        color: var(--newsprint-fg);
        line-height: 1.6;
        resize: none;
        font-family: 'Lora', serif;
        min-height: 130px;
        box-sizing: border-box;
        
        &::placeholder {
          color: var(--newsprint-fg-muted);
        }
      }
    }
  }
  
  .search-controls {
    position: absolute;
    bottom: 8px;
    left: 12px;
    right: 12px;
    display: flex;
    justify-content: flex-end;
    align-items: center;
    pointer-events: none;
    
    > * {
      pointer-events: auto;
    }
  }
  
  .search-send-container {
    display: flex;
    align-items: center;
    gap: 8px;
    
    .shortcut-hint {
      color: var(--newsprint-fg-muted);
      font-size: 12px;
      font-weight: 400;
      text-transform: uppercase;
      letter-spacing: 0.05em;
    }
    
    .send-button {
      background: var(--newsprint-fg);
      color: var(--newsprint-bg);
      border: 2px solid var(--newsprint-fg);
      padding: 8px;
      font-size: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      
      &:hover {
        background: var(--newsprint-accent);
        border-color: var(--newsprint-accent);
        box-shadow: 4px 4px 0px 0px var(--newsprint-fg);
      }
      
      &:active {
        transform: translateY(2px);
      }
    }
  }
}

.examples-section {
  max-width: 1100px;
  margin: 0 auto;
  padding-top: 5px;
  
  .section-title {
    text-align: center;
    font-size: 24px;
    font-weight: 700;
    color: var(--newsprint-fg);
    margin-bottom: 5px;
    text-transform: uppercase;
    letter-spacing: 0.1em;
    
    .section-subtitle {
      display: block;
      font-size: 14px;
      font-weight: 400;
      color: var(--newsprint-fg-muted);
      margin-top: 4px;
      text-transform: none;
      letter-spacing: normal;
    }
  }
  
  .examples-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 18px;
    margin-top: 12px;
    
    .example-card {
      background: var(--newsprint-neutral-100);
      padding: 15px;
      cursor: pointer;
      transition: all 0.3s ease;
      border: 2px solid var(--newsprint-fg);
      position: relative;
      overflow: hidden;
      
      &:hover {
        transform: translate(-4px, -4px);
        box-shadow: 8px 8px 0px 0px var(--newsprint-fg);
      }
      
      .example-header {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 8px;
        
        .example-icon {
          width: 40px;
          height: 40px;
          background: var(--newsprint-accent);
          display: flex;
          align-items: center;
          justify-content: center;
          color: var(--newsprint-bg);
          flex-shrink: 0;
        }
        
        .example-title-wrapper {
          flex: 1;
          
          .example-title {
            font-size: 16px;
            font-weight: 700;
            color: var(--newsprint-fg);
            margin: 0 0 4px 0;
            text-transform: uppercase;
            letter-spacing: 0.05em;
          }
          
          .example-category {
            background: var(--newsprint-bg);
            color: var(--newsprint-accent);
            padding: 3px 10px;
            font-size: 11px;
            font-weight: 500;
            white-space: nowrap;
            border: 1px solid var(--newsprint-accent);
            text-transform: uppercase;
            letter-spacing: 0.05em;
          }
        }
      }
      
      .example-description {
        color: var(--newsprint-fg-muted);
        line-height: 1.4;
        margin-bottom: 10px;
        font-size: 13px;
        font-family: 'Lora', serif;
      }
      
      .example-action {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: var(--newsprint-accent);
        font-weight: 600;
        font-size: 13px;
        margin-bottom: 12px;
        text-transform: uppercase;
        letter-spacing: 0.05em;
      }
      
      .example-preview {
        height: 60px;
        background: var(--newsprint-bg);
        padding: 8px;
        border: 1px solid var(--newsprint-border);
        
        .robot-preview {
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          height: 100%;
          position: relative;
          
          .assembly-icon {
            width: 24px;
            height: 24px;
            background: var(--newsprint-accent);
            position: relative;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: var(--newsprint-bg);
          }
          
          .assembly-tools {
            display: flex;
            align-items: center;
            gap: 4px;
            
            .tool-box {
              width: 8px;
              height: 6px;
              background: var(--newsprint-fg);
            }
            
            .connector {
              width: 12px;
              height: 2px;
              background: var(--newsprint-fg);
            }
            
            .component {
              width: 6px;
              height: 6px;
              background: var(--newsprint-accent);
            }
          }
        }
        
        .search-preview {
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          height: 100%;
          position: relative;
          
          .search-container {
            display: flex;
            align-items: center;
            gap: 6px;
            margin-bottom: 8px;
            
            .search-box-icon {
              width: 14px;
              height: 14px;
              background: var(--newsprint-accent);
              display: flex;
              align-items: center;
              justify-content: center;
              color: var(--newsprint-bg);
            }
            
            .search-box {
              width: 35px;
              height: 12px;
              background: var(--newsprint-bg);
              border: 2px solid var(--newsprint-fg);
              position: relative;
            }
          }
          
          .search-waves {
            position: absolute;
            bottom: 8px;
            left: 50%;
            transform: translateX(-50%);
            display: flex;
            gap: 2px;
            
            .wave {
              width: 3px;
              background: var(--newsprint-accent);
              
              &.wave1 { height: 4px; }
              &.wave2 { height: 6px; }
              &.wave3 { height: 5px; }
            }
          }
        }
        
        .news-preview {
          padding: 6px;
          background: var(--newsprint-neutral-100);
          border: 1px solid var(--newsprint-fg);
          position: relative;
          
          .news-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            
            .news-title {
              width: 70%;
              height: 8px;
              background: var(--newsprint-fg);
            }
            
            .news-date {
              width: 20%;
              height: 4px;
              background: var(--newsprint-fg-muted);
            }
          }
          
          .news-content {
            .news-line {
              height: 4px;
              background: var(--newsprint-fg);
              margin-bottom: 3px;
              
              &.long { width: 100%; }
              &.medium { width: 75%; }
              &.short { width: 45%; }
            }
          }
          
          .news-badge {
            position: absolute;
            top: 4px;
            right: 4px;
            background: var(--newsprint-accent);
            color: var(--newsprint-bg);
            font-size: 8px;
            font-weight: 700;
            padding: 2px 4px;
            text-transform: uppercase;
          }
        }
        
        .pie-preview {
          display: flex;
          justify-content: center;
          align-items: center;
          height: 100%;
          
          .pie-chart {
            width: 50px;
            height: 50px;
            position: relative;
            background: conic-gradient(
              var(--newsprint-accent) 0deg 120deg, 
              var(--newsprint-fg) 120deg 240deg, 
              var(--newsprint-fg-muted) 240deg
            );
            
            &::before {
              content: '';
              position: absolute;
              top: 50%;
              left: 50%;
              transform: translate(-50%, -50%);
              width: 20px;
              height: 20px;
              background: var(--newsprint-bg);
            }
            
            &::after {
              content: '';
              position: absolute;
              top: 50%;
              left: 50%;
              transform: translate(-50%, -50%);
              width: 8px;
              height: 8px;
              background: var(--newsprint-accent);
            }
          }
        }
      }
    }
  }
}

@media (max-width: 768px) {
  .homepage {
    padding: 20px 10px;
  }
  
  .logo-section {
    .logo-container {
      flex-direction: column;
      gap: 12px;
      
      .brand-name {
        font-size: 36px;
      }
    }
  }
  
  .search-section {
    .search-container {
      padding: 24px;
      
      .search-box .search-input-wrapper {
        min-height: 140px;
        
        .search-input {
          min-height: 100px;
        }
      }
      
      .search-controls {
        bottom: 8px;
        left: 16px;
        right: 16px;
        
        .search-send-container {
          .shortcut-hint {
            display: none;
          }
          
          .send-button {
            width: 36px;
            height: 36px;
            font-size: 18px;
          }
        }
      }
    }
  }
  
  .examples-section {
    .examples-grid {
      grid-template-columns: 1fr;
    }
  }
}
</style>