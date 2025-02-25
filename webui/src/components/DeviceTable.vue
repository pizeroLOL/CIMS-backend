<template>
  <div class="device-table">
    <table>
      <thead>
        <tr>
          <th>名称</th>
          <th>UID</th>
          <th>状态</th>
          <th>当前课程</th>
          <th>管理</th>
        </tr>
      </thead>
      <tbody>
        <DeviceTableRow
          v-for="(clientId, clientUid) in clients"
          :key="clientUid"
          :clientId="clientId"
          :clientUid="clientUid"
          :isOnline="getClientOnlineStatus(clientUid)"
          @open-management="openManagementDialog"
        />
      </tbody>
    </table>
    <ClientStatusDialog v-if="isManagingClient" :clientUid="managingClientUid" @close="closeManagementDialog" /> <!-- 设备管理对话框 -->
  </div>
</template>

<script>
import DeviceTableRow from './DeviceTableRow.vue';
import ClientStatusDialog from './ClientStatusDialog.vue'; // 导入 ClientStatusDialog

export default {
  name: 'DeviceTable',
  components: {
    DeviceTableRow,
    ClientStatusDialog // 注册 ClientStatusDialog
  },
  props: {
    clients: {
      type: Object,
      required: true
    },
    clientStatuses: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      managingClientUid: null // 当前正在管理的客户端 UID
    };
  },
  computed: {
    isManagingClient() {
      return !!this.managingClientUid; // managingClientUid 有值时返回 true，否则返回 false
    }
  },
  methods: {
    getClientOnlineStatus(clientUid) {
      return this.clientStatuses && this.clientStatuses[clientUid] ? this.clientStatuses[clientUid].isOnline : false;
    },
    openManagementDialog(clientUid) {
      this.managingClientUid = clientUid; // 设置 managingClientUid，显示对话框
    },
    closeManagementDialog() {
      this.managingClientUid = null; // 清空 managingClientUid，关闭对话框
    }
  }
};
</script>

<style scoped>
.device-table {
  width: 100%;
  overflow-x: auto; /* 水平滚动条，如果表格内容超出宽度 */
}

.device-table table {
  border-collapse: collapse;
  width: 100%;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden; /* 确保圆角 */
}

.device-table th,
.device-table td {
  padding: 12px 15px;
  text-align: left;
  border-bottom: 1px solid #eee;
}

.device-table th {
  background-color: #f0f0f0;
  font-weight: bold;
}

.device-table tbody tr:last-child td {
  border-bottom: none; /* 移除最后一行的底边框 */
}

.device-table td:last-child {
  text-align: center; /* 最后一列居中对齐 */
}
</style>