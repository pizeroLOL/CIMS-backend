<template>
  <fluent-card class="overview-card">
    <h3 class="card-title">{{ title }}</h3>
    <div class="card-content">
      <slot></slot>
    </div>
  </fluent-card>
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

<style>
.overview-card {
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 20px;
  margin-bottom: 20px;
  background-color: white;
}

.card-title {
  margin-top: 0;
  margin-bottom: 15px;
  color: #333;
}

.card-content {
  color: #555;
}
</style>