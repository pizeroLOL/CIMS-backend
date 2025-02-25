<template>
  <div class="file-editor">
    <h3>{{ fileName }} 文件管理</h3>
    <ul v-if="fileList && fileList.length > 0">
      <li v-for="file in fileList" :key="file" @click="loadFileContent(file)" style="cursor: pointer;">
        {{ file }}
      </li>
    </ul>
    <p v-else>没有文件。</p>

    <fluent-panel v-if="currentFileContent !== null" :hidden="false" @dismiss="currentFileContent = null">
      <span slot="header">
        <h4>编辑文件: {{ currentFileName }}</h4>
      </span>
      <span slot="body">
        <fluent-textarea v-model="currentFileContent" resizable style="width: 100%; min-height: 300px; font-family: monospace;"></fluent-textarea>
      </span>
      <span slot="footer">
        <fluent-button @click="saveFileContent" :disabled="isSaving" appearance="primary">
          <span v-if="!isSaving">保存文件</span>
          <span v-else>保存中...</span>
        </fluent-button>
        <fluent-button @click="currentFileContent = null" :disabled="isSaving">关闭编辑器</fluent-button>
      </span>
    </fluent-panel>

    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'FileEditor',
  props: {
    fileName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      fileList: null,
      currentFileName: null,
      currentFileContent: null,
      errorMessage: null,
      isSaving: false,
    };
  },
  mounted() {
    this.fetchFileList();
  },
  methods: {
    async fetchFileList() {
      this.errorMessage = null;
      try {
        const response = await axios.get(`/api/v1/resources/${this.fileName}`);
        this.fileList = response.data;
      } catch (error) {
        console.error(`获取 ${this.fileName} 文件列表失败:`, error);
        this.fileList = [];
        this.errorMessage = `获取文件列表失败: ${error.message}`;
      }
    },
    async loadFileContent(file) {
      this.errorMessage = null;
      try {
        const response = await axios.get(`/api/v1/resources/${this.fileName}/${file}`);
        this.currentFileName = file;
        this.currentFileContent = JSON.stringify(response.data, null, 2);
      } catch (error) {
        console.error(`加载文件 ${file} 内容失败:`, error);
        this.currentFileContent = null;
        this.errorMessage = `加载文件内容失败: ${error.message}`;
      }
    },
    async saveFileContent() {
      this.errorMessage = null;
      this.isSaving = true;
      try {
        const parsedContent = JSON.parse(this.currentFileContent);
        await axios.post(`/api/v1/resources/${this.fileName}/${this.currentFileName}`, { content: parsedContent });
        alert(`文件 ${this.currentFileName} 已保存`);
      } catch (error) {
        console.error(`保存文件 ${this.currentFileName} 内容失败:`, error);
        this.errorMessage = `保存文件内容失败: ${error.message}`;
      } finally {
        this.isSaving = false;
      }
    }
  }
};
</script>

<style>
/* 可以在全局 CSS 或组件的 style 中添加 Web Components 的样式 */
.file-editor .error-message {
  color: red;
  margin-top: 10px;
}
</style>