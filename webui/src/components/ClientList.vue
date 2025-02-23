<template>
  <div class="client-list">
    <h3>客户端列表</h3>
    <div class="client-card-container" v-if="clients && Object.keys(clients).length > 0">
      <ClientCard
        v-for="(clientId, clientUid) in clients"
        :key="clientUid"
        :clientUid="clientUid"
        :clientId="clientId"
        :isOnline="getClientOnlineStatus(clientUid)"
        @select-client="$emit('select-client', $event)"
      />
    </div>
    <p v-else>没有客户端注册。</p>
  </div>
</template>

<script>
import axios from 'axios';
import ClientCard from './ClientCard.vue';

export default {
  name: 'ClientList',
  components: {
    ClientCard
  },
  emits: ['select-client'],
  data() {
    return {
      clients: null,
      clientStatuses: null // 用于存储客户端状态
    };
  },
  mounted() {
    this.fetchClientsAndStatuses();
    this.interval = setInterval(this.fetchClientStatuses, 10000); // 每 10 秒更新客户端状态
  },
  beforeUnmount() {
    clearInterval(this.interval); // 组件卸载时清除定时器
  },
  methods: {
    async fetchClientsAndStatuses() {
      await Promise.all([
        this.fetchClients(),
        this.fetchClientStatuses()
      ]);
    },
    async fetchClients() {
      try {
        const response = await axios.get('/command/clients');
        this.clients = response.data;
      } catch (error) {
        console.error("获取客户端列表失败:", error);
        this.clients = {}; // 确保 clients 为对象而不是 null，以便 Object.keys() 可以使用
      }
    },
    async fetchClientStatuses() {
      try {
        const response = await axios.get('/command/clients/status');
        this.clientStatuses = response.data;
      } catch (error) {
        console.error("获取客户端状态失败:", error);
        this.clientStatuses = {};
      }
    },
    getClientOnlineStatus(clientUid) {
      return this.clientStatuses && this.clientStatuses[clientUid] ? this.clientStatuses[clientUid].isOnline : false;
    }
  }
};
</script>

<style scoped>
.client-list {
  margin-bottom: 20px;
}

.client-card-container {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr)); /* 响应式网格布局 */
  gap: 15px;
}
</style>