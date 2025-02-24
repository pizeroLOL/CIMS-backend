<template>
  <div class="notification-dialog" v-if="show">
    <div class="dialog-content">
      <h3>发送通知 - 客户端 UID: {{ clientUid }}</h3>
      <label for="messageMask">消息遮罩:</label>
      <input type="text" id="messageMask" v-model="notificationData.message_mask">

      <label for="messageContent">消息内容:</label>
      <textarea id="messageContent" v-model="notificationData.message_content"></textarea>

      <div class="checkbox-group">
        <label><input type="checkbox" v-model="notificationData.is_emergency"> 紧急消息</label>
        <label><input type="checkbox" v-model="notificationData.is_speech_enabled"> 语音播报</label>
        <label><input type="checkbox" v-model="notificationData.is_effect_enabled"> 特效</label>
        <label><input type="checkbox" v-model="notificationData.is_sound_enabled"> 声音</label>
        <label><input type="checkbox" v-model="notificationData.is_topmost"> 置顶显示</label>
      </div>

      <label for="durationSeconds">显示持续时间 (秒):</label>
      <input type="number" id="durationSeconds" v-model.number="notificationData.duration_seconds">

      <label for="repeatCounts">重复次数:</label>
      <input type="number" id="repeatCounts" v-model.number="notificationData.repeat_counts">

      <div class="buttons">
        <button @click="sendNotification">发送通知</button>
        <button @click="closeDialog">取消</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'NotificationSenderDialog',
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
      notificationData: {
        message_mask: '',
        message_content: '',
        overlay_icon_left: 0,
        overlay_icon_right: 0,
        is_emergency: false,
        is_speech_enabled: true,
        is_effect_enabled: true,
        is_sound_enabled: true,
        is_topmost: true,
        duration_seconds: 5,
        repeat_counts: 1
      }
    };
  },
  methods: {
    async sendNotification() {
      try {
        const queryParams = new URLSearchParams(this.notificationData).toString();
        const url = `/command/clients/${this.clientUid}/notify?${queryParams}`;

        await axios.post(url);
        this.$parent.showNotification(`已向客户端 ${this.clientUid} 发送通知`, 'success'); // 替换 alert
        this.closeDialog();
      } catch (error) {
        console.error("发送通知失败:", error);
        this.$parent.showNotification("发送通知失败", 'error'); // 替换 alert
      }
    },
    closeDialog() {
      this.$emit('close');
    }
  }
};
</script>