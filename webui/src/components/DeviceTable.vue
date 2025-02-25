<template>
  <div class="device-table">
    <fluent-grid class="table">
      <div class="thead">
        <fluent-grid-row class="tr">
          <fluent-grid-cell class="th">名称</fluent-grid-cell>
          <fluent-grid-cell class="th">UID</fluent-grid-cell>
          <fluent-grid-cell class="th">状态</fluent-grid-cell>
          <fluent-grid-cell class="th">当前课程</fluent-grid-cell>
          <fluent-grid-cell class="th">管理</fluent-grid-cell>
        </fluent-grid-row>
      </div>
      <div class="tbody">
        <DeviceTableRow
          v-for="(clientId, clientUid) in clients"
          :key="clientUid"
          :clientId="clientId"
          :clientUid="clientUid"
          :isOnline="getClientOnlineStatus(clientUid)"
          @open-management="openManagementDialog"
        />
      </div>
    </fluent-grid>
    <ClientStatusDialog v-if="isManagingClient" :clientUid="managingClientUid" @close="closeManagementDialog" />
  </div>
</template>

<script>
import DeviceTableRow from './DeviceTableRow.vue';
import ClientStatusDialog from './ClientStatusDialog.vue';

export default {
  name: 'DeviceTable',
  components: {
    DeviceTableRow,
    ClientStatusDialog
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
      managingClientUid: null
    };
  },
  computed: {
    isManagingClient() {
      return !!this.managingClientUid;
    }
  },
  methods: {
    getClientOnlineStatus(clientUid) {
      return this.clientStatuses && this.clientStatuses[clientUid] ? this.clientStatuses[clientUid].isOnline : false;
    },
    openManagementDialog(clientUid) {
      this.managingClientUid = clientUid;
    },
    closeManagementDialog() {
      this.managingClientUid = null;
    }
  }
};
</script>

<style>
.device-table {
  width: 100%;
  overflow-x: auto;
}

.table {
  display: block; /* 使用 display:block 让 fluent-grid 表现为块级元素 */
  border-collapse: collapse;
  width: 100%;
  background-color: white;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border-radius: 8px;
  overflow: hidden;
}

.thead {
  display: block; /* 使用 display:block 让 thead 表现为块级元素 */
}

.tbody {
  display: block; /* 使用 display:block 让 tbody 表现为块级元素 */
}


.tr {
  display: grid; /* 使用 display:grid 创建网格布局 */
  grid-template-columns: repeat(5, 1fr); /* 定义 5 列均分宽度 */
  border-bottom: 1px solid #eee;
}

.tr:last-child {
  border-bottom: none; /* 移除最后一行的底边框 */
}

.th, .td {
  padding: 12px 15px;
  text-align: left;
  display: block; /* 让 th 和 td 块级显示以填充网格单元 */
  overflow: hidden; /* 确保内容不会溢出单元格 */
  text-overflow: ellipsis; /* 超出部分显示省略号 */
  white-space: nowrap; /* 防止文本换行 */
}


.th {
  background-color: #f0f0f0;
  font-weight: bold;
}

.td:last-child {
  text-align: center; /* 最后一列居中对齐 */
}
</style>