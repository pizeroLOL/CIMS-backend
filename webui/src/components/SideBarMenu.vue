<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <img src="../assets/logo.png" alt="ClassIsland Logo" class="logo">
      <div class="app-title">ClassIsland<br>集控控制台</div>
    </div>
    <nav class="main-nav">
      <ul>
        <li>
          <router-link to="/" :class="{ active: $route.name === 'Overview' }">概览</router-link>
        </li>
        <li>
          <router-link to="/devices" :class="{ active: $route.name === 'DeviceManagement' }">设备管理</router-link>
        </li>
        <li>
          <router-link to="/resources" :class="{ active: $route.name === 'ResourceManagement' }">资源管理</router-link>
        </li>
        <li>
          <router-link to="/settings" :class="{ active: $route.name === 'Settings' }">设置</router-link>
        </li>
      </ul>
    </nav>
    <div class="webui-version">
      WebUI 版本 v0.1.0 <br>
      后端版本 v1.1.7
    </div>
  </div>
</template>

<script>
export default {
  name: 'SideBarMenu'
}
</script>

<style scoped>
.sidebar {
  width: 220px;
  background-color: #00838f; /* 深青色背景 */
  color: white;
  padding: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.sidebar-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-bottom: 40px;
}

.logo {
  width: 60px;
  height: 60px;
  margin-bottom: 10px;
}

.app-title {
  font-size: 1.2em;
  font-weight: bold;
  text-align: center;
  line-height: 1.2;
}


.main-nav ul {
  list-style: none;
  padding: 0;
  margin: 0;
  width: 100%;
}

.main-nav li {
  margin-bottom: 10px;
}

.main-nav li:last-child {
  margin-bottom: 0;
}

.main-nav a {
  display: block;
  padding: 10px 15px;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  transition: background-color 0.2s ease-in-out;
  text-align: left; /* 文本左对齐 */
}

.main-nav a:hover,
.main-nav a.router-link-active {
  background-color: rgba(255, 255, 255, 0.1); /* 悬停和激活状态浅色背景 */
}

.main-nav a.router-link-active {
  font-weight: bold;
}

.webui-version {
  margin-top: auto; /* 推到侧边栏底部 */
  font-size: 0.8em;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
}
</style>