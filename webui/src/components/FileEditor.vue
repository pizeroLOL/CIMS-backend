<template>
  <div class="file-editor">
    <h3>{{ fileName }} 文件管理</h3>
    <ul v-if="fileList && fileList.length > 0">
      <li v-for="file in fileList" :key="file" @click="loadFileContent(file)" style="cursor: pointer;">
        {{ file }}
      </li>
    </ul>
    <p v-else>没有文件。</p>

    <div v-if="currentFileContent !== null" class="editor-area">
      <h4>编辑文件: {{ currentFileName }}</h4>
      <textarea v-model="currentFileContent" style="width: 100%; min-height: 300px; font-family: monospace;"></textarea>
      <div class="editor-buttons">
        <button @click="saveFileContent" :disabled="isSaving">
          <span v-if="!isSaving">保存文件</span>
          <span v-else>保存中...</span>
        </button>
        <button @click="currentFileContent = null" :disabled="isSaving">关闭编辑器</button>
      </div>
    </div>
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
      isSaving: false, // 加载状态
    };
  },
  mounted() {
    this.fetchFileList();
  },
  methods: {
    async fetchFileList() {
      this.errorMessage = null; // 清空错误信息
      try {
        const response = await axios.get(`/api/v1/resources/${this.fileName}`); // 调用新的文件列表 API
        this.fileList = response.data;
      } catch (error) {
        console.error(`获取 ${this.fileName} 文件列表失败:`, error);
        this.fileList = [];
        this.errorMessage = `获取文件列表失败: ${error.message}`;
      }
    },
    async loadFileContent(file) {
      this.errorMessage = null; // 清空错误信息
      try {
        const response = await axios.get(`/api/v1/resources/${this.fileName}/${file}`); // 调用新的获取文件内容 API
        this.currentFileName = file;
        this.currentFileContent = JSON.stringify(response.data, null, 2); // 格式化 JSON
      } catch (error) {
        console.error(`加载文件 ${file} 内容失败:`, error);
        this.currentFileContent = null;
        this.errorMessage = `加载文件内容失败: ${error.message}`;
      }
    },
    async saveFileContent() {
      this.errorMessage = null; // 清空错误信息
      this.isSaving = true; // 设置为保存中状态
      try {
        const parsedContent = JSON.parse(this.currentFileContent); // 尝试解析 JSON
        await axios.post(`/api/v1/resources/${this.fileName}/${this.currentFileName}`, { content: parsedContent }); // 调用新的保存文件内容 API，发送 JSON 内容
        alert(`文件 ${this.currentFileName} 已保存`);
      } catch (error) {
        console.error(`保存文件 ${this.currentFileName} 内容失败:`, error);
        this.errorMessage = `保存文件内容失败: ${error.message}`;
      } finally {
        this.isSaving = false; // 恢复状态
      }
    }
  }
};
</script>

<style scoped>
/* ... (样式保持不变) ... */
.editor-buttons button {
  margin-top: 10px;
  margin-right: 10px;
  padding: 8px 15px;
  cursor: pointer;
}
.error-message {
  color: red;
  margin-top: 10px;
}
</style>