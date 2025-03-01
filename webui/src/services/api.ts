import axios from 'axios';

export const apiClient = axios.create({
  baseURL: '/', // 代理已经配置在 vite.config.ts 中
});