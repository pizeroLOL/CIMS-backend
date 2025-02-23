<template>
  <div class="resources-view">
    <h2>资源管理</h2>
    <FileEditor fileName="Manifests" />
    <FileEditor fileName="Policies" />
    <FileEditor fileName="ClassPlans" />
    <FileEditor fileName="SubjectsSource" />
    <FileEditor fileName="TimeLayouts" />
    <FileEditor fileName="DefaultSettings" />
  </div>
</template>

<script>
import FileEditor from '../components/FileEditor.vue';

export default {
  name: 'ResourcesView',
  components: {
    FileEditor
  }
};
</script>

<style scoped>
.resources-view {
  padding: 20px;
}
</style>