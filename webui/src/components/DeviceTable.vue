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
        />
      </tbody>
    </table>
  </div>
</template>

<script>
import DeviceTableRow from './DeviceTableRow.vue';

export default {
  name: 'DeviceTable',
  components: {
    DeviceTableRow
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
  methods: {
    getClientOnlineStatus(clientUid) {
      return this.clientStatuses && this.clientStatuses[clientUid] ? this.clientStatuses[clientUid].isOnline : false;
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