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
        // 构建 URL 查询字符串
        const queryParams = new URLSearchParams(this.notificationData).toString();
        const url = `/command/clients/${this.clientUid}/notify?${queryParams}`;

        await axios.post(url); // 使用 POST 请求，但不再发送请求体，参数已在 URL 中
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

<style scoped>
.notification-dialog {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1001;
}

.dialog-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  width: 600px;
  max-height: 90vh;
  overflow-y: auto;
}

.notification-dialog label {
  display: block;
  margin-top: 10px;
  margin-bottom: 5px;
  font-weight: bold;
}

.notification-dialog input[type="text"],
.notification-dialog input[type="number"],
.notification-dialog textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.notification-dialog textarea {
  font-family: inherit; /* 继承父级字体 */
  min-height: 100px;
}


.checkbox-group {
  display: flex;
  flex-direction: column; /* 垂直排列复选框 */
  margin-bottom: 10px;
}

.checkbox-group label {
  font-weight: normal; /* 复选框标签不加粗 */
  margin: 5px 0;
  display: flex; /* 使标签和复选框对齐 */
  align-items: center; /* 垂直居中对齐 */
}

.checkbox-group input[type="checkbox"] {
  margin-right: 5px; /* 复选框和文字之间留出间距 */
}


.buttons {
  margin-top: 20px;
  text-align: right;
}

.buttons button {
  margin-left: 10px;
  padding: 8px 15px;
  cursor: pointer;
}
</style>