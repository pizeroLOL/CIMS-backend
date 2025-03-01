import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'

// https://vitejs.dev/config/
export default defineConfig({
  plugins: [react()],
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:50050',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '/api') // 确保路径正确重写
      },
      '/command': {
        target: 'http://localhost:50052',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/command/, '/command') // 确保路径正确重写
      }
    }
  }
})