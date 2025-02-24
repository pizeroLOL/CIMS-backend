<template>
  <div class="overview-view">
    <OverviewCard title="设备在线状态">
      <p>当前 {{ onlineDeviceCount }} 台设备在线</p>
      <p>本地共注册 {{ totalDeviceCount }} 台设备</p>
    </OverviewCard>
  </div>
</template>

<script>
import OverviewCard from '../components/OverviewCard.vue';
import axios from 'axios';

export default {
  name: 'OverviewView',
  components: {
    OverviewCard
  },
  data() {
    return {
      onlineDeviceCount: 0,
      totalDeviceCount: 0,
      clientStatuses: {}
    };
  },
  mounted() {
    this.fetchData();
    this.interval = setInterval(this.fetchData, 10000); // 每 10 秒更新数据
  },
  beforeUnmount() {
    clearInterval(this.interval);
  },
  methods: {
    async fetchData() {
      try {
        const clientsResponse = await axios.get('/command/clients');
        const statusResponse = await axios.get('/command/clients/status');
        this.clientStatuses = statusResponse.data;
        this.totalDeviceCount = Object.keys(clientsResponse.data).length;
        this.onlineDeviceCount = Object.values(this.clientStatuses).filter(status => status.isOnline).length;

      } catch (error) {
        console.error("获取概览数据失败:", error);
      }
    }
  }
};
</script>

<style scoped>
.overview-view {
  padding: 20px;
}
</style>