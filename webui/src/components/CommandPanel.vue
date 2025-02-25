<template>
  <div class="command-panel">
    <h3>客户端命令</h3>
    <button @click="restartClient">重启客户端</button>
    <button @click="openNotificationDialog">发送通知</button>
    <NotificationSenderDialog v-if="showNotificationDialog" :clientUid="clientUid" @close="showNotificationDialog = false" />
    <button @click="updateClientData">更新客户端数据</button>
  </div>
</template>

<script>
import axios from 'axios';
import NotificationSenderDialog from './NotificationSenderDialog.vue';

export default {
  name: 'CommandPanel',
  components: {
    NotificationSenderDialog
  },
  props: {
    clientUid: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      showNotificationDialog: false
    };
  },
  methods: {
    async restartClient() {
      try {
        await axios.post(`/command/clients/${this.clientUid}/restart`);
        this.$parent.showNotification(`已向客户端 ${this.clientUid} 发送重启命令`, 'success'); // 替换 alert
      } catch (error) {
        console.error("发送重启命令失败:", error);
        this.$parent.showNotification("发送重启命令失败", 'error'); // 替换 alert
      }
    },
    openNotificationDialog() {
      this.showNotificationDialog = true;
    },
    async updateClientData() {
      try {
        await axios.post(`/command/clients/${this.clientUid}/update`);
        this.$parent.showNotification(`已向客户端 ${this.clientUid} 发送数据更新命令`, 'success'); // 替换 alert
      } catch (error) {
        console.error("发送数据更新命令失败:", error);
        this.$parent.showNotification("发送数据更新命令失败", 'error'); // 替换 alert
      }
    }
  }
};
</script>

<style scoped>
.command-panel button {
  margin-right: 10px;
  padding: 8px 15px;
  cursor: pointer;
}
</style>