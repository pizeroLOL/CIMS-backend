<template>
  <div id="app">
    <aside class="sidebar">
      <div class="sidebar-header">
        <img src="./assets/logo.png" alt="集控管理中心 Logo" class="logo">
        <h3>集控管理</h3>
      </div>
      <nav class="main-nav">
        <ul>
          <li>
            <router-link to="/" exact>
              <i class="icon home"></i> 首页
            </router-link>
          </li>
          <li>
            <router-link to="/clients">
              <i class="icon clients"></i> 客户端管理
            </router-link>
          </li>
          <li>
            <router-link to="/resources">
              <i class="icon resources"></i> 资源管理
            </router-link>
          </li>
        </ul>
      </nav>
    </aside>
    <main class="main-content">
      <router-view />
    </main>
    <app-notification ref="notification" />
  </div>
</template>

<script>
import AppNotification from './components/AppNotification.vue';

export default {
  components: {
    AppNotification
  },
  methods: {
    showNotification(message, type = 'info', duration = 3000) {
      this.$refs.notification.showNotification(message, type, duration);
    }
  }
};
</script>

<style>
/* 基础样式重置 */
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f4f4;
  color: #333;
}

#app {
  display: flex;
  max-width: 1600px;
  margin: 20px auto;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

/* 侧边栏样式 */
.sidebar {
  width: 250px;
  background-color: #f8f9fa;
  border-right: 1px solid #eee;
  padding: 20px;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  text-align: center;
  margin-bottom: 30px;
}

.logo {
  width: 80px;
  height: 80px;
  margin-bottom: 10px;
}

.sidebar-header h3 {
  margin: 0;
  color: #0078d4;
}

.main-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.main-nav li {
  padding: 0;
  margin-bottom: 10px;
}

.main-nav li:last-child {
  margin-bottom: 0;
}

.main-nav a {
  display: block;
  padding: 10px 15px;
  color: #333;
  text-decoration: none;
  border-radius: 6px;
  transition: background-color 0.2s ease-in-out;
}

.main-nav a:hover,
.main-nav a.router-link-active {
  background-color: #e9ecef;
  color: #0078d4;
}

/* 主内容区域样式 */
.main-content {
  flex-grow: 1;
  padding: 20px;
}

/* 页面内容基础样式 */
.home,
.clients-view,
.resources-view {
  padding: 20px;
}
</style>