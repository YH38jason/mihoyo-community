import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/Home.vue'

const routes = [
  {
    path: '/',
    component: () => import('../components/tohome.vue')
  },
  {
    path: '/home',
    name: 'home',
    component: HomeView
  },
  {
    path: '/dev',
    name: 'div',
    component: () => import('../components/dev.vue')
  },
  {
    path: '/read/:id',
    component: () => import('../components/read.vue'),
  },
  {
    path: '/support',
    component: () => import('@/components/spt.vue')
  },
  {
    path: '/newpost',
    component: () => import('@/components/newpost.vue')
  },
  {
    path: '/error',
    component: () => import('../components/error.vue'),
  },
  {
    path: '/themes',
    component: () => import('../views/Themes.vue')
  },
  {
    path: '/theme/:theme',
    component: () => import('../views/Theme.vue')
  },
  {
    path: '/live/genshin',
    component: () => import('../components/live.vue')
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
