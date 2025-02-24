const { defineConfig } = require('@vue/cli-service')
module.exports = defineConfig({
  transpileDependencies: true,
  devServer: {
    port: 50053,
    proxy: {
      '/command': {
        target: 'http://localhost:50052',
        changeOrigin: true
      }
    }
  }
})