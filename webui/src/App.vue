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
      <router-view/>
    </main>
  </div>
</template>

<script>
export default {
  name: 'App',
  components: {
  }
};
</script>

<style>
body {
  font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f4f4f4;
  color: #333;
}

#app {
  display: flex; /* 使用 Flexbox 布局 */
  max-width: 1600px; /* 增大最大宽度 */
  margin: 20px auto;
  background-color: #fff;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden; /* 确保圆角正确显示 */
}

/* 侧边栏样式 */
.sidebar {
  width: 250px; /* 固定宽度 */
  background-color: #f8f9fa; /* 浅灰色背景 */
  border-right: 1px solid #eee;
  padding: 20px;
  display: flex;
  flex-direction: column; /* 垂直布局 */
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
  color: #0078d4; /* 品牌主色 */
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
  background-color: #e9ecef; /* 悬停和激活状态背景色 */
  color: #0078d4; /* 悬停和激活状态文字颜色 */
}


/* 主内容区域样式 */
.main-content {
  flex-grow: 1; /* 占据剩余空间 */
  padding: 20px;
}

.home {
  padding: 20px;
}

.clients-view,
.resources-view {
  padding: 20px;
}
</style>