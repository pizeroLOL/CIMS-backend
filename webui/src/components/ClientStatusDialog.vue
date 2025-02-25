<template>
  <fluent-dialog :hidden="!show" @dismiss="closeDialog" title-text="客户端状态 - UID: {{ clientUid }}" is-modeless>
    <template v-slot:title>  <!-- 替换为 <template v-slot:title> -->
      客户端状态 - UID: {{ clientUid }}
    </template>
    <template v-slot:body>   <!-- 替换为 <template v-slot:body> -->
      <p><strong>在线状态:</strong> {{ clientStatus.isOnline ? '在线' : '离线' }}</p>
      <p><strong>上次心跳:</strong> {{ new Date(clientStatus.lastHeartbeat * 1000).toLocaleString() }}</p>

      <CommandPanel :clientUid="clientUid" />
    </template>
    <template v-slot:footer>  <!-- 替换为 <template v-slot:footer> -->
      <fluent-button @click="closeDialog">关闭</fluent-button>
    </template>
  </fluent-dialog>
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
    },
    show: {
      type: Boolean,
      default: true
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
    },
    closeDialog() {
      this.$emit('close');
    }
  }
};
</script>

<style>
/* 可以在全局 CSS 或组件的 style 中添加 Web Components 的样式 */
</style>