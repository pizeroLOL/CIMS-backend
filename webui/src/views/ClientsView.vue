<template>
  <div class="clients-view">
    <h2>客户端管理</h2>
    <ClientList @select-client="selectedClientUid = $event" />
    <ClientStatusDialog v-if="selectedClientUid" :clientUid="selectedClientUid" @close="selectedClientUid = null" />
  </div>
</template>

<script>
import ClientList from '../components/ClientList.vue';
import ClientStatusDialog from '../components/ClientStatusDialog.vue';

export default {
  name: 'ClientsView',
  components: {
    ClientList,
    ClientStatusDialog
  },
  data() {
    return {
      selectedClientUid: null
    };
  }
};
</script>

<style scoped>
.clients-view {
  padding: 20px;
}
</style>