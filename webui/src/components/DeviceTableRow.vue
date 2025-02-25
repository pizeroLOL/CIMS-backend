<template>
  <tr>
    <td>{{ clientId }}</td>
    <td>{{ clientUid }}</td>
    <td>
      <span v-if="isOnline" class="status-online">在线</span>
      <span v-else class="status-offline">离线</span>
    </td>
    <td>晚自习</td>
    <td><a @click="$emit('open-management', clientUid)" style="cursor: pointer;">管理 ></a></td> <!-- 修改后的管理链接 -->
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
  },
  emits: ['open-management'] // 声明组件会触发 'open-management' 事件
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