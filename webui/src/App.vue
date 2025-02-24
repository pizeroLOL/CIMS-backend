<template>
  <div id="app">
    <Sidebar />
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
    Sidebar: SideBarMenu
  }
}
</script>

<style scoped>
#app {
  display: flex;
  font-family: '微软雅黑', sans-serif;
  height: 100vh;
  overflow: hidden;
}

.content-area {
  flex: 1;
  background-color: #e0f7fa; /* 淡蓝色背景 */
  padding: 20px;
  overflow-y: auto;
}
</style>