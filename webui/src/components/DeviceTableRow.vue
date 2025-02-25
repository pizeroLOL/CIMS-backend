<template>
  <fluent-grid-row class="tr">
    <fluent-grid-cell class="td">{{ clientId }}</fluent-grid-cell>
    <fluent-grid-cell class="td">{{ clientUid }}</fluent-grid-cell>
    <fluent-grid-cell class="td">
      <span v-if="isOnline" class="status-online">在线</span>
      <span v-else class="status-offline">离线</span>
    </fluent-grid-cell>
    <fluent-grid-cell class="td">晚自习</fluent-grid-cell>
    <fluent-grid-cell class="td"><a @click="$emit('open-management', clientUid)" style="cursor: pointer;">管理 ></a></fluent-grid-cell>
  </fluent-grid-row>
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
  emits: ['open-management']
}
</script>

<style>
.tr {
  display: grid; /* 确保 row 也是 grid 布局，继承父级的 grid-template-columns */
  grid-template-columns: inherit; /* 继承父级的列定义 */
}


.status-online {
  color: green;
}

.status-offline {
  color: red;
}
</style>