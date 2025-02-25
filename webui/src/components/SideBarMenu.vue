<template>
  <div class="sidebar">
    <div class="sidebar-header">
      <img src="../assets/logo.png" alt="ClassIsland Logo" class="logo">
      <div class="app-title">ClassIsland<br>集控控制台</div>
    </div>
    <fluent-nav>
      <fluent-nav-group>
        <fluent-nav-item href="/" :active="$route.path === '/'">概览</fluent-nav-item>
        <fluent-nav-item href="/devices" :active="$route.path === '/devices'">设备管理</fluent-nav-item>
        <fluent-nav-item href="/resources" :active="$route.path === '/resources'">资源管理</fluent-nav-item>
        <fluent-nav-item href="/settings" :active="$route.path === '/settings'">设置</fluent-nav-item>
      </fluent-nav-group>
    </fluent-nav>
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

<style>
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

.webui-version {
  margin-top: auto; /* 推到侧边栏底部 */
  font-size: 0.8em;
  text-align: center;
  color: rgba(255, 255, 255, 0.7);
}

fluent-nav {
  width: 100%; /* 让 fluent-nav 占据侧边栏宽度 */
}

fluent-nav-group {
  width: 100%; /* 让 fluent-nav-group 占据 fluent-nav 宽度 */
}

fluent-nav-item {
  display: block; /* 让 fluent-nav-item 块级显示以填充宽度 */
  padding: 10px 15px;
  color: white;
  text-decoration: none;
  border-radius: 6px;
  margin-bottom: 10px; /* 保持链接之间的间距 */
  transition: background-color 0.2s ease-in-out;
  text-align: left;
}

fluent-nav-item:hover,
fluent-nav-item[active] {
  background-color: rgba(255, 255, 255, 0.1); /* 悬停和激活状态浅色背景 */
}

fluent-nav-item[active] {
  font-weight: bold;
}
</style>