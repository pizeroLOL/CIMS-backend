<template>
  <div class="client-card" @click="$emit('select-client', clientUid)">
    <div class="card-header">
      <span class="client-id">{{ clientId }}</span>
    </div>
    <div class="card-body">
      <p><strong>UID:</strong> {{ clientUid }}</p>
      <p v-if="isOnline" class="online-status">
        <span class="status-indicator online"></span> 在线
      </p>
      <p v-else class="offline-status">
        <span class="status-indicator offline"></span> 离线
      </p>

      <div class="profile-config">
        <h4>配置文件</h4>
        <div class="profile-item" v-for="profileType in profileTypes" :key="profileType">
          <label>{{ profileType }}:</label>
          <select v-model="clientProfileConfig[profileType]" @change="onProfileConfigChange">
            <option v-for="name in profileNames[profileType]" :key="name" :value="name">{{ name }}</option>
          </select>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ClientCard',
  props: {
    clientUid: {
      type: String,
      required: true
    },
    clientId: {
      type: String,
      required: true
    },
    isOnline: {
      type: Boolean,
      default: false
    }
  },
  emits: ['select-client'],
  data() {
    return {
      profileTypes: ['ClassPlan', 'Settings', 'Subjects', 'Policy', 'TimeLayout'],
      profileNames: { // 存储各个 Profile 类型的可用名称
        'ClassPlan': [],
        'Settings': [],
        'Subjects': [],
        'Policy': [],
        'TimeLayout': []
      },
      clientProfileConfig: {} // 存储客户端的 Profile 配置
    };
  },
  mounted() {
    this.fetchProfileNames();
    this.fetchClientProfileConfig();
  },
  methods: {
    async fetchProfileNames() {
      for (const profileType of this.profileTypes) {
        try {
          const response = await axios.get(`/api/v1/profiles/names/${profileType}`);
          this.profileNames[profileType] = response.data;
        } catch (error) {
          console.error(`获取 ${profileType} 配置文件名列表失败:`, error);
          this.profileNames[profileType] = [];
        }
      }
    },
    async fetchClientProfileConfig() {
      try {
        const response = await axios.get(`/api/v1/client/${this.clientUid}/profileConfig`);
        this.clientProfileConfig = response.data;
        // 初始化配置，如果某些 profileType 没有配置，则设置为 "default"
        this.profileTypes.forEach(type => {
          if (!this.clientProfileConfig[type]) {
            // 使用直接赋值替换 this.$set
            this.clientProfileConfig[type] = 'default';
          }
        });
      } catch (error) {
        console.error(`获取客户端 ${this.clientUid} 配置文件失败:`, error);
        this.clientProfileConfig = {};
        // 初始化配置为 "default"
        this.profileTypes.forEach(type => {
          // 使用直接赋值替换 this.$set
          this.clientProfileConfig[type] = 'default';
        });
      }
    },
    async saveClientProfileConfig() {
      try {
        await axios.post(`/api/v1/client/${this.clientUid}/profileConfig`, this.clientProfileConfig);
        alert(`客户端 ${this.clientUid} 配置文件已保存`);
      } catch (error) {
        console.error(`保存客户端 ${this.clientUid} 配置文件失败:`, error);
        alert(`保存客户端 ${this.clientUid} 配置文件失败`);
      }
    },
    onProfileConfigChange() {
      this.saveClientProfileConfig(); // 每次配置更改后自动保存
    }
  }
};
</script>

<style scoped>
.client-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.client-card:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.card-header {
  background-color: #0078d4; /* Fluent Design Primary Color */
  color: white;
  padding: 12px 15px;
  text-align: left;
  font-weight: bold;
}

.card-body {
  padding: 15px;
  text-align: left;
}

.client-id {
  font-size: 1.2em;
}

.status-indicator {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 5px;
}

.online-status .status-indicator {
  background-color: #28a745; /* Green for online */
}

.offline-status .status-indicator {
  background-color: #dc3545; /* Red for offline */
}

.profile-config {
  margin-top: 15px;
  border-top: 1px solid #eee;
  padding-top: 15px;
}

.profile-item {
  margin-bottom: 10px;
  display: flex;
  align-items: center;
}

.profile-item label {
  margin-right: 10px;
  width: 80px;
  text-align: right;
}

.profile-item select {
  flex-grow: 1;
  padding: 8px;
  border-radius: 4px;
  border: 1px solid #ccc;
}
</style>