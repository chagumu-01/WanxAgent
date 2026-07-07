import { loadEnv, defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'
import AutoImport from 'unplugin-auto-import/vite'
import Components from 'unplugin-vue-components/vite'
import { ElementPlusResolver } from 'unplugin-vue-components/resolvers'
import path from 'path'

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd())

  return {
    resolve: {
      alias: {
        '@': path.resolve(__dirname, 'src')
      }
    },
    server: {
      host: '0.0.0.0',
      port: Number(env.VITE_DEV_PORT) || 8091,
      https: false,
      proxy: {
        '/api': {
          target: env.VITE_API_BASE_URL || 'http://localhost:7860',
          changeOrigin: true,
        },
        '/local_storage': {
          target: env.VITE_API_BASE_URL || 'http://localhost:7860',
          changeOrigin: true,
        }
      }
    },
    plugins: [
      vue(),
      AutoImport({ resolvers: [ElementPlusResolver()] }),
      Components({ resolvers: [ElementPlusResolver()] }),
    ],
    css: {
      preprocessorOptions: {
        scss: {
          additionalData: `
            @use "sass:color";
            @import "@/assets/styles/variable.scss";
          `
        }
      }
    }
  }
})
