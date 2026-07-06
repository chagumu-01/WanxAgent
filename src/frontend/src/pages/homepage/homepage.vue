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
    iconColor: '#c41e3a'
  },
  {
    title: '深度搜索',
    category: '搜索模式',
    description: '连接外部互联网资源，扩展系统能力和数据源',
    action: '开始搜索 →',
    icon: Search,
    iconColor: '#d94560'
  },
  {
    title: 'AI日报',
    category: '生成模式',
    description: '对最近的AI新闻进行整理总结，可生成下载链接',
    action: '生成日报 →',
    icon: Newspaper,
    iconColor: '#e87187'
  },
  {
    title: '知识库问答',
    category: '知识库模式',
    description: '基于已有知识库进行精准问答和信息检索',
    action: '查询知识 →',
    icon: FileText,
    iconColor: '#c41e3a'
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
                  fill="none" stroke="#c41e3a" stroke-width="8"/>
            <path d="M30 50 C30 50 45 30 50 35 C55 30 70 50 70 50" 
                  fill="none" stroke="#c41e3a" stroke-width="8" stroke-linecap="round"/>
            <path d="M30 50 C30 50 45 70 50 65 C55 70 70 50 70 50" 
                  fill="none" stroke="#c41e3a" stroke-width="8" stroke-linecap="round"/>
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
  background: linear-gradient(135deg, #fceef2 0%, #f8d0d8 50%, #f2a5b5 100%);
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
      background: #ffffff;
      border-radius: 16px;
      display: flex;
      align-items: center;
      justify-content: center;
      border: 3px solid #c41e3a;
      box-shadow: 0 8px 24px rgba(196, 30, 58, 0.4);
      animation: float 3s ease-in-out infinite;
      
      .logo-svg {
        width: 40px;
        height: 40px;
      }
    }
    
    .brand-name {
      font-size: 48px;
      font-weight: 800;
      color: #c41e3a;
      margin: 0;
      position: relative;
      letter-spacing: -1px;
      
      &::after {
        content: '';
        position: absolute;
        bottom: -8px;
        left: 0;
        right: 0;
        height: 3px;
        background: linear-gradient(90deg, transparent, #c41e3a, #d94560, #c41e3a, transparent);
        border-radius: 2px;
        opacity: 0.6;
      }
    }
  }
  
  .brand-slogan {
    font-size: 16px;
    color: #c41e3a;
    margin-top: 12px;
    font-weight: 500;
    letter-spacing: 2px;
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
    background: #ffffff;
    border-radius: 22px;
    padding: 32px;
    box-shadow: 0 12px 40px rgba(196, 30, 58, 0.12);
    border: 1px solid #f2a5b5;
  }
  
  .search-box {
    margin-bottom: 18px;
    
    .search-input-wrapper {
      background: #fceef2;
      border-radius: 16px;
      padding: 14px;
      border: 2px solid #f2a5b5;
      transition: all 0.3s ease;
      min-height: 160px;
      width: 100%;
      display: block;
      position: relative;
      
      &:focus-within {
        border-color: #c41e3a;
        box-shadow: 0 0 0 4px rgba(196, 30, 58, 0.1);
      }
      
      .search-input {
        width: 100%;
        border: none;
        background: transparent;
        padding: 12px 18px 45px 18px;
        font-size: 19px;
        outline: none;
        color: #4a1a25;
        line-height: 1.6;
        resize: none;
        font-family: inherit;
        min-height: 130px;
        box-sizing: border-box;
        
        &::placeholder {
          color: #d94560;
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
      color: #d94560;
      font-size: 12px;
      font-weight: 400;
    }
    
    .send-button {
      background: linear-gradient(135deg, #c41e3a, #d94560);
      color: white;
      border: none;
      padding: 8px;
      border-radius: 8px;
      font-size: 16px;
      cursor: pointer;
      transition: all 0.2s ease;
      width: 32px;
      height: 32px;
      display: flex;
      align-items: center;
      justify-content: center;
      box-shadow: 0 2px 6px rgba(196, 30, 58, 0.3);
      
      &:hover {
        background: linear-gradient(135deg, #9e1830, #c41e3a);
        box-shadow: 0 3px 8px rgba(196, 30, 58, 0.4);
        transform: translateY(-1px);
      }
      
      &:active {
        transform: translateY(0);
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
    color: #4a1a25;
    margin-bottom: 5px;
    
    .section-subtitle {
      display: block;
      font-size: 14px;
      font-weight: 400;
      color: #c41e3a;
      margin-top: 4px;
    }
  }
  
  .examples-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
    gap: 18px;
    margin-top: 12px;
    
    .example-card {
      background: #ffffff;
      border-radius: 16px;
      padding: 15px;
      cursor: pointer;
      transition: all 0.3s ease;
      border: 1px solid #f2a5b5;
      position: relative;
      overflow: hidden;
      box-shadow: 0 3px 8px rgba(196, 30, 58, 0.05);
      
      &:hover {
        transform: translateY(-8px);
        box-shadow: 0 20px 40px rgba(196, 30, 58, 0.15);
        border-color: #e87187;
      }
      
      .example-header {
        display: flex;
        align-items: flex-start;
        gap: 12px;
        margin-bottom: 8px;
        
        .example-icon {
          width: 40px;
          height: 40px;
          border-radius: 12px;
          display: flex;
          align-items: center;
          justify-content: center;
          color: white;
          flex-shrink: 0;
          box-shadow: 0 4px 12px rgba(196, 30, 58, 0.2);
        }
        
        .example-title-wrapper {
          flex: 1;
          
          .example-title {
            font-size: 16px;
            font-weight: 600;
            color: #4a1a25;
            margin: 0 0 4px 0;
          }
          
          .example-category {
            background: #fceef2;
            color: #c41e3a;
            padding: 3px 10px;
            border-radius: 10px;
            font-size: 11px;
            font-weight: 500;
            white-space: nowrap;
          }
        }
      }
      
      .example-description {
        color: #c41e3a;
        line-height: 1.4;
        margin-bottom: 10px;
        font-size: 13px;
      }
      
      .example-action {
        display: flex;
        align-items: center;
        justify-content: space-between;
        color: #c41e3a;
        font-weight: 500;
        font-size: 13px;
        margin-bottom: 12px;
      }
      
      .example-preview {
        height: 60px;
        border-radius: 8px;
        background: #fceef2;
        padding: 8px;
        
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
            background: linear-gradient(135deg, #c41e3a, #d94560);
            border-radius: 6px;
            position: relative;
            margin-bottom: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            box-shadow: 0 2px 6px rgba(196, 30, 58, 0.3);
          }
          
          .assembly-tools {
            display: flex;
            align-items: center;
            gap: 4px;
            
            .tool-box {
              width: 8px;
              height: 6px;
              background: linear-gradient(135deg, #c41e3a, #9e1830);
              border-radius: 2px;
              box-shadow: 0 1px 2px rgba(196, 30, 58, 0.3);
            }
            
            .connector {
              width: 12px;
              height: 2px;
              background: #c41e3a;
              border-radius: 1px;
            }
            
            .component {
              width: 6px;
              height: 6px;
              background: linear-gradient(135deg, #10b981, #059669);
              border-radius: 50%;
              box-shadow: 0 1px 2px rgba(16, 185, 129, 0.3);
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
              background: #c41e3a;
              border-radius: 50%;
              display: flex;
              align-items: center;
              justify-content: center;
              color: white;
            }
            
            .search-box {
              width: 35px;
              height: 12px;
              background: linear-gradient(135deg, #f8d0d8, #f2a5b5);
              border: 2px solid #c41e3a;
              border-radius: 8px;
              position: relative;
              box-shadow: 0 0 0 1px rgba(196, 30, 58, 0.3);
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
              background: linear-gradient(to top, #c41e3a, #d94560);
              border-radius: 2px;
              
              &.wave1 { height: 4px; }
              &.wave2 { height: 6px; }
              &.wave3 { height: 5px; }
            }
          }
        }
        
        .news-preview {
          padding: 6px;
          background: linear-gradient(135deg, #fefefe, #fceef2);
          border: 1px solid #f2a5b5;
          border-radius: 4px;
          position: relative;
          
          .news-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 8px;
            
            .news-title {
              width: 70%;
              height: 8px;
              background: linear-gradient(90deg, #c41e3a, #d94560);
              border-radius: 2px;
              box-shadow: 0 1px 3px rgba(196, 30, 58, 0.3);
            }
            
            .news-date {
              width: 20%;
              height: 4px;
              background: #94a3b8;
              border-radius: 2px;
            }
          }
          
          .news-content {
            .news-line {
              height: 4px;
              background: linear-gradient(90deg, #c41e3a, #94a3b8);
              border-radius: 2px;
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
            background: linear-gradient(135deg, #c41e3a, #d94560);
            color: white;
            font-size: 8px;
            font-weight: 700;
            padding: 2px 4px;
            border-radius: 3px;
            box-shadow: 0 1px 3px rgba(196, 30, 58, 0.4);
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
            border-radius: 50%;
            position: relative;
            background: conic-gradient(
              #c41e3a 0deg 120deg, 
              #d94560 120deg 240deg, 
              #e87187 240deg
            );
            box-shadow: 0 4px 12px rgba(196, 30, 58, 0.4);
            
            &::before {
              content: '';
              position: absolute;
              top: 50%;
              left: 50%;
              transform: translate(-50%, -50%);
              width: 20px;
              height: 20px;
              background: white;
              border-radius: 50%;
              box-shadow: 0 2px 6px rgba(0, 0, 0, 0.1);
            }
            
            &::after {
              content: '';
              position: absolute;
              top: 50%;
              left: 50%;
              transform: translate(-50%, -50%);
              width: 8px;
              height: 8px;
              background: linear-gradient(45deg, #c41e3a, #d94560);
              border-radius: 50%;
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