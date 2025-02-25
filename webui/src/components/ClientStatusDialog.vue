        <template>
  <div v-if="clientStatus" class="client-status-dialog">
    <div class="dialog-content">
      <h3>客户端状态 - UID: {{ clientUid }}</h3>
      <p><strong>在线状态:</strong> {{ clientStatus.isOnline ? '在线' : '离线' }}</p>
      <p><strong>上次心跳:</strong> {{ new Date(clientStatus.lastHeartbeat * 1000).toLocaleString() }}</p>

      <CommandPanel :clientUid="clientUid" />

      <button @click="$emit('close')">关闭</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import CommandPanel from './CommandPanel.vue';

export default {
  name: 'ClientStatusDialog',
  components: {
    CommandPanel
  },
  props: {
    clientUid: {
      type: String,
      required: true
    }
  },
  emits: ['close'],
  data() {
    return {
      clientStatus: null
    };
  },
  mounted() {
    this.fetchClientStatus();
  },
  methods: {
    async fetchClientStatus() {
      try {
        const response = await axios.get(`/command/clients/${this.clientUid}/status`);
        this.clientStatus = response.data;
      } catch (error) {
        console.error("获取客户端状态失败:", error);
        this.clientStatus = null;
      }
    }
  }
};
</script>

<style scoped>
.client-status-dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.dialog-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: 500px;
}

.dialog-content h3 {
  margin-top: 0;
}

.dialog-content button {
  margin-top: 15px;
  padding: 8px 15px;
  cursor: pointer;
}
</style>