<template>
  <fluent-dialog v-if="show" @dismiss="closeDialog" title-text="发送通知" is-modeless>
    <template v-slot:body>
      <fluent-form>
        <fluent-form-group label="消息遮罩:">
          <fluent-text-field v-model="notificationData.message_mask" placeholder="请输入消息遮罩"></fluent-text-field>
        </fluent-form-group>
        <fluent-form-group label="消息内容:">
          <fluent-textarea v-model="notificationData.message_content" placeholder="请输入消息内容" resizable></fluent-textarea>
        </fluent-form-group>
        <fluent-form-group label="提醒设置:">
          <fluent-checkbox v-model="notificationData.is_emergency" label="紧急消息"></fluent-checkbox>
          <fluent-checkbox v-model="notificationData.is_speech_enabled" label="语音播报"></fluent-checkbox>
          <fluent-checkbox v-model="notificationData.is_effect_enabled" label="特效"></fluent-checkbox>
          <fluent-checkbox v-model="notificationData.is_sound_enabled" label="声音"></fluent-checkbox>
          <fluent-checkbox v-model="notificationData.is_topmost" label="置顶显示"></fluent-checkbox>
        </fluent-form-group>
        <fluent-form-group label="显示设置:">
          <fluent-number-field v-model.number="notificationData.duration_seconds" label="持续时间 (秒)" min="1" step="1"></fluent-number-field>
          <fluent-number-field v-model.number="notificationData.repeat_counts" label="重复次数" min="1" step="1"></fluent-number-field>
        </fluent-form-group>
      </fluent-form>
    </template>
    <template v-slot:footer>
      <fluent-button @click="sendNotification" appearance="primary">发送通知</fluent-button>
      <fluent-button @click="closeDialog">取消</fluent-button>
    </template>
  </fluent-dialog>
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
        alert(`已向客户端 ${this.clientUid} 发送通知`);
        this.closeDialog();
      } catch (error) {
        console.error("发送通知失败:", error);
        alert("发送通知失败");
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