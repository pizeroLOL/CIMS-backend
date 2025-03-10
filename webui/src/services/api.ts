import axios from 'axios';

const apiBaseUrl = import.meta.env.VITE_API_BASE_URL;
const commandBaseUrl = import.meta.env.VITE_COMMAND_BASE_URL;

if (!apiBaseUrl) {
  throw new Error("环境变量 VITE_API_BASE_URL 未设置，请配置该变量。");
}

if (!commandBaseUrl) {
  throw new Error("环境变量 VITE_COMMAND_BASE_URL 未设置，请配置该变量。");
}

export const apiClient = axios.create({
  baseURL: '/',
});

apiClient.interceptors.request.use(
  (config) => {
    if (config.url?.startsWith('/api')) {
      config.baseURL = apiBaseUrl || '/api';
    } else if (config.url?.startsWith('/command')) {
      config.baseURL = commandBaseUrl || '/command';
    } else {
      config.baseURL = '/';
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);