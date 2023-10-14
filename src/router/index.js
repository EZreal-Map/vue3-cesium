import { createRouter, createWebHistory } from 'vue-router'
import FloodView from '@/views/FloodView.vue'
import NotFound from '@/views/NotFound.vue'

const yearsOptions = ['5years', '30years', '50years']

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      redirect: '/flood/30years'
    },
    {
      path: '/flood',
      redirect: '/flood/30years'
    },
    {
      path: '/flood/:years',
      name: 'flood',
      component: FloodView,
      beforeEnter: (to, from, next) => {
        const yearsParam = to.params.years
        if (yearsOptions.includes(yearsParam)) {
          next() // 如果在指定的数组范围内，继续导航
        } else {
          next('/flood/404') // 否则导航到 NotFound 组件或其他适当的路由
        }
      }
    },
    {
      path: '/flood/404',
      name: 'NotFound',
      component: NotFound
    },
    {
      path: '/:catchAll(.*)',
      component: NotFound
    }
  ]
})

export default router
