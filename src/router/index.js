import Vue from 'vue'
import VueRouter from 'vue-router'
import Full from '../components/Full.vue'
import Main from '../components/Main.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/full',
    name: 'Full',
    component: Full
  },
  {
    path: '/',
    name: 'Main',
    component: Main
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
