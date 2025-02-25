<template>
  <div class="command-panel">
    <h3>客户端命令</h3>
    <fluent-button appearance="primary" @click="restartClient">重启客户端</fluent-button>
    <fluent-button @click="openNotificationDialog">发送通知</fluent-button>
    <NotificationSenderDialog v-if="showNotificationDialog" :clientUid="clientUid" @close="showNotificationDialog = false" />
    <fluent-button @click="updateClientData">更新客户端数据</fluent-button>
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
        alert(`已向客户端 ${this.clientUid} 发送重启命令`);
      } catch (error) {
        console.error("发送重启命令失败:", error);
        alert("发送重启命令失败");
      }
    },
    openNotificationDialog() {
      this.showNotificationDialog = true;
    },
    async updateClientData() {
      try {
        await axios.post(`/command/clients/${this.clientUid}/update`);
        alert(`已向客户端 ${this.clientUid} 发送数据更新命令`);
      } catch (error) {
        console.error("发送数据更新命令失败:", error);
        alert("发送数据更新命令失败");
      }
    }
  }
};
</script>

<style>
.command-panel fluent-button {
  margin-right: 10px;
}
</style>