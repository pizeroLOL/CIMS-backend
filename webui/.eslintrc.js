module.exports = {
  root: true,
  env: {
    node: true,
  },
  'extends': [
    'plugin:vue/vue3-essential', // Vue 3 Essential 规则集
    'eslint:recommended'         // ESLint 推荐规则集
  ],
  parserOptions: {
    parser: '@babel/eslint-parser' // 使用 babel-eslint 解析器
  },
  rules: {
    // 这里可以添加自定义的 ESLint 规则
    'no-console': process.env.NODE_ENV === 'production' ? 'warn' : 'off', // 生产环境警告 console 语句
    'no-debugger': process.env.NODE_ENV === 'production' ? 'warn' : 'off' // 生产环境警告 debugger 语句
  }
};