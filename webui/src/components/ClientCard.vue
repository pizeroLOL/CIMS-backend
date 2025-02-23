<template>
  <div class="client-card" @click="$emit('select-client', clientUid)">
    <div class="card-header">
      <span class="client-id">{{ clientId }}</span>
    </div>
    <div class="card-body">
      <p><strong>UID:</strong> {{ clientUid }}</p>
      <p v-if="isOnline" class="online-status">
        <span class="status-indicator online"></span> 在线
      </p>
      <p v-else class="offline-status">
        <span class="status-indicator offline"></span> 离线
      </p>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ClientCard',
  props: {
    clientUid: {
      type: String,
      required: true
    },
    clientId: {
      type: String,
      required: true
    },
    isOnline: {
      type: Boolean,
      default: false
    }
  },
  emits: ['select-client']
};
</script>

<style scoped>
.client-card {
  background-color: #fff;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  margin-bottom: 15px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.client-card:hover {
  transform: scale(1.02);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.card-header {
  background-color: #0078d4; /* Fluent Design Primary Color */
  color: white;
  padding: 12px 15px;
  text-align: left;
  font-weight: bold;
}

.card-body {
  padding: 15px;
  text-align: left;
}

.client-id {
  font-size: 1.2em;
}

.status-indicator {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  margin-right: 5px;
}

.online-status .status-indicator {
  background-color: #28a745; /* Green for online */
}

.offline-status .status-indicator {
  background-color: #dc3545; /* Red for offline */
}
</style>