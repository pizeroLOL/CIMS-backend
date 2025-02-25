<template>
  <fluent-dialog :hidden="!show" @dismiss="closeDialog" title-text="客户端配置" is-modeless>
    <span slot="body">
      <fluent-form>
        <fluent-form-group v-for="(configType, currentConfigName) in clientConfig" :key="configType" :label="configType + ':'">
          <fluent-select v-model="localClientConfig[configType]">
            <fluent-option value="default">default.json</fluent-option>
            <!-- 未来可以动态加载更多配置文件选项 -->
          </fluent-select>
        </fluent-form-group>
      </fluent-form>
    </span>
    <span slot="footer">
      <fluent-button @click="saveConfig" appearance="primary">保存配置</fluent-button>
      <fluent-button @click="closeDialog">取消</fluent-button>
    </span>
  </fluent-dialog>
</template>

<script>
import axios from 'axios';

export default {
  name: 'ClientConfigDialog',
  props: {
    clientUid: {
      type: String,
      required: true,
    },
    show: {
      type: Boolean,
      default: true
    }
  },
  emits: ['close'],
  data() {
    return {
      clientId: null,
      clientConfig: {},
      localClientConfig: {},
    };
  },
  async mounted() {
    await this.fetchClientInfo();
    await this.loadProfileConfig();
  },
  methods: {
    async fetchClientInfo() {
      try {
        const response = await axios.get(`/command/clients`);
        const clients = response.data;
        this.clientId = clients[this.clientUid];
      } catch (error) {
        console.error("获取客户端信息失败:", error);
      }
    },
    async loadProfileConfig() {
      try {
        const response = await axios.get(`/api/v1/profileconfig`);
        const profileConfig = response.data;
        this.clientConfig = profileConfig[this.clientUid] || {};
        this.localClientConfig = { ...this.clientConfig };
      } catch (error) {
        console.error("加载 profile_config.json 失败:", error);
      }
    },
    async saveConfig() {
      try {
        await axios.post('/api/v1/profileconfig', {
          clientUid: this.clientUid,
          config: this.localClientConfig
        });
        alert('客户端配置已保存');
        this.closeDialog();
      } catch (error) {
        console.error("保存客户端配置失败:", error);
        alert('保存客户端配置失败');
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