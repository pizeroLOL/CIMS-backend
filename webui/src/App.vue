<template>
  <div id="app">
    <SideBarMenu />
    <div class="content-area">
      <router-view />
    </div>
  </div>
</template>

<script>
import SideBarMenu from './components/SideBarMenu.vue'

export default {
  name: 'App',
  components: {
    SideBarMenu
  }
}
</script>

<style>
/* 全局样式，因为 Web Components 的 scoped 样式可能不太适用 */
body {
  font-family: 'Segoe UI', sans-serif;
  margin: 0;
  padding: 0;
}

#app {
  display: flex;
  height: 100vh;
  overflow: hidden;
}

.content-area {
  flex: 1;
  background-color: #f3f2f1; /* Fluent UI Light Gray Background */
  padding: 20px;
  overflow-y: auto;
}
</style>