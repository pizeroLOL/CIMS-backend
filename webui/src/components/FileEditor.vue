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
      <button @click="saveFileContent">保存文件</button>
      <button @click="currentFileContent = null">关闭编辑器</button>
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
      currentFileContent: null
    };
  },
  mounted() {
    this.fetchFileList();
  },
  methods: {
    async fetchFileList() {
      try {
        // 假设 API 端点是 /api/files/{fileName}，返回文件名列表
        // 需要后端提供获取文件列表的 API
        this.fileList = [`${this.fileName}1.json`, `${this.fileName}2.json`, `${this.fileName}3.json`]; // 模拟数据
      } catch (error) {
        console.error(`获取 ${this.fileName} 文件列表失败:`, error);
        this.fileList = [];
      }
    },
    async loadFileContent(file) {
      try {
        // 假设 API 端点是 /api/files/{fileName}/{file}，返回文件内容
        const response = await axios.get(`/api/v1/client/default/${this.fileName.toLowerCase()}`); // 假设后端接口直接返回文件内容
        this.currentFileName = file;
        this.currentFileContent = JSON.stringify(response.data, null, 2); // 格式化 JSON
      } catch (error) {
        console.error(`加载文件 ${file} 内容失败:`, error);
        this.currentFileContent = null;
      }
    },
    async saveFileContent() {
      try {
        // 假设 API 端点是 /api/files/{fileName}/{file}，POST 请求保存文件内容
        // 后端需要实现保存文件的 API
        alert('保存功能待后端API实现'); // 提示保存功能待实现
        // await axios.post(`/api/files/${this.fileName}/${this.currentFileName}`, { content: this.currentFileContent });
        // alert(`文件 ${this.currentFileName} 已保存`);
      } catch (error) {
        console.error(`保存文件 ${this.currentFileName} 内容失败:`, error);
        alert(`保存文件 ${this.currentFileName} 内容失败`);
      }
    }
  }
};
</script>

<style scoped>
.file-editor {
  margin-bottom: 20px;
}

.file-editor ul {
  list-style-type: none;
  padding: 0;
}

.file-editor li {
  padding: 8px 12px;
  border-bottom: 1px solid #eee;
}

.file-editor li:last-child {
  border-bottom: none;
}

.file-editor li:hover {
  background-color: #f0f0f0;
}

.editor-area {
  margin-top: 20px;
  border: 1px solid #ccc;
  padding: 10px;
  border-radius: 4px;
}

.editor-area h4 {
  margin-top: 0;
}

.editor-area button {
  margin-top: 10px;
  margin-right: 10px;
  padding: 8px 15px;
  cursor: pointer;
}
</style>