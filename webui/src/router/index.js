import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import ClientsView from '../views/ClientsView.vue'
import ResourcesView from '../views/ResourcesView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/clients',
    name: 'clients',
    component: ClientsView
  },
  {
    path: '/resources',
    name: 'resources',
    component: ResourcesView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router