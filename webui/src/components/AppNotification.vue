<template>
  <div v-if="isShow" class="notification-container" :class="typeClass">
    <div class="notification-content">
      <p>{{ notificationMessage }}</p>
      <button class="close-button" @click="closeNotification">
        <svg viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg"><path d="M18.5 5.5L5.5 18.5M5.5 5.5L18.5 18.5" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
      </button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AppNotification', // 修改组件名为 AppNotification
  props: {
    message: {
      type: String,
      default: ''
    },
    type: {
      type: String,
      default: 'info', // info, success, warning, error
      validator: value => ['info', 'success', 'warning', 'error'].includes(value)
    },
    duration: {
      type: Number, // milliseconds
      default: 3000
    }
  },
  data() {
    return {
      isShow: false, // 使用 isShow 替换 show
      notificationMessage: '', // 使用 notificationMessage 替换 message
      notificationType: 'info', // 使用 notificationType 替换 type
      notificationDuration: 3000, // 使用 notificationDuration 替换 duration
      timer: null
    };
  },
  computed: {
    typeClass() {
      return `notification-${this.notificationType}`; // 使用 notificationType
    }
  },
  watch: {
    isShow(newValue) { // 监听 isShow
      if (newValue && this.notificationDuration > 0) { // 使用 notificationDuration
        this.timer = setTimeout(() => {
          this.isShow = false;
        }, this.notificationDuration); // 使用 notificationDuration
      } else if (!newValue && this.timer) {
        clearTimeout(this.timer);
        this.timer = null;
      }
    }
  },
  methods: {
    showNotification(msg = this.message, t = this.type, dur = this.duration) { // showNotification 方法参数保持不变
      this.notificationMessage = msg; // 更新 data 属性
      this.notificationType = t; // 更新 data 属性
      this.notificationDuration = dur; // 更新 data 属性
      this.isShow = true; // 更新 data 属性
    },
    closeNotification() {
      this.isShow = false;
    }
  }
};
</script>

<style scoped>
.notification-container {
  position: fixed;
  top: 20px;
  right: 20px;
  z-index: 1002; /* 确保在其他元素之上 */
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
  overflow: hidden;
  opacity: 0.95; /* 半透明 */
}

.notification-content {
  padding: 15px 20px;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.notification-content p {
  margin: 0;
  flex-grow: 1;
}

.close-button {
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  margin-left: 15px;
  opacity: 0.6;
  transition: opacity 0.2s ease-in-out;
}

.close-button:hover {
  opacity: 1;
}

.close-button svg {
  width: 18px;
  height: 18px;
  display: block;
}

/* 类型样式 */
.notification-info {
  border-left: 4px solid #2196F3; /* Info blue */
}

.notification-success {
  border-left: 4px solid #4CAF50; /* Success green */
}

.notification-warning {
  border-left: 4px solid #FF9800; /* Warning orange */
}

.notification-error {
  border-left: 4px solid #F44336; /* Error red */
}
</style>