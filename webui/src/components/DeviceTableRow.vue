<template>
  <tr>
    <td>{{ clientId }}</td>
    <td>{{ clientUid }}</td>
    <td>
      <span v-if="isOnline" class="status-online">在线</span>
      <span v-else class="status-offline">离线</span>
    </td>
    <td>晚自习</td> <!-- 示例数据，实际数据可能需要从后端获取 -->
    <td><a href="#">管理 ></a></td>
  </tr>
</template>

<script>
export default {
  name: 'DeviceTableRow',
  props: {
    clientId: {
      type: String,
      required: true
    },
    clientUid: {
      type: String,
      required: true
    },
    isOnline: {
      type: Boolean,
      default: false
    }
  }
}
</script>

<style scoped>
.status-online {
  color: green;
}

.status-offline {
  color: red;
}
</style>