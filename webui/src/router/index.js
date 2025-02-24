import { createRouter, createWebHistory } from 'vue-router'
import OverviewView from '../views/OverviewView.vue'
import DeviceManagementView from '../views/DeviceManagementView.vue'
import ResourceManagementView from '../views/ResourceManagementView.vue'
import SettingsView from '../views/SettingsView.vue'

const routes = [
  {
    path: '/',
    name: 'Overview',
    component: OverviewView
  },
  {
    path: '/devices',
    name: 'DeviceManagement',
    component: DeviceManagementView
  },
  {
    path: '/resources',
    name: 'ResourceManagement',
    component: ResourceManagementView
  },
  {
    path: '/settings',
    name: 'Settings',
    component: SettingsView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router