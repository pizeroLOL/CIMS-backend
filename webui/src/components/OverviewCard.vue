<template>
  <div class="overview-card">
    <h3>{{ title }}</h3>
    <div class="card-content">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: 'OverviewCard',
  props: {
    title: {
      type: String,
      required: true
    }
  }
}
</script>

<style scoped>
.overview-card {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
}

.overview-card h3 {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
}

.card-content {
  color: #555;
}
</style>