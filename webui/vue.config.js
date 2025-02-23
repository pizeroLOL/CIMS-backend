const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 50053, // 指定开发服务器端口为 50053
    proxy: {
      '/api': { // 将以 /api 开头的请求代理到 Python 后端 API 服务器
        target: 'http://localhost:50050',
        changeOrigin: true
      },
      '/command': { // 将以 /command 开头的请求代理到 Python 后端 Command 服务器
        target: 'http://localhost:50052',
        changeOrigin: true
      }
    }
  }
})