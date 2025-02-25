<template>
  <div class="device-management-view">
    <h2>设备管理</h2>
    <DeviceTable :clientStatuses="clientStatuses" :clients="clients" />
  </div>
</template>

<script>
import DeviceTable from '../components/DeviceTable.vue';
import axios from 'axios';

export default {
  name: 'DeviceManagementView',
  components: {
    DeviceTable
  },
  data() {
    return {
      clients: {},
      clientStatuses: {}
    };
  },
  mounted() {
    this.fetchData();
    this.interval = setInterval(this.fetchData, 10000);
  },
  beforeUnmount() {
    clearInterval(this.interval);
  },
  methods: {
    async fetchData() {
      try {
        const clientsResponse = await axios.get('/command/clients');
        const statusResponse = await axios.get('/command/clients/status');
        this.clients = clientsResponse.data;
        this.clientStatuses = statusResponse.data;
      } catch (error) {
        console.error("获取设备管理数据失败:", error);
      }
    }
  }
};
</script>

<style>
/* 可以在全局 CSS 或组件的 style 中添加 Web Components 的样式 */
</style>