import { createRouter, createWebHistory } from 'vue-router'
import FloodView from '@/views/FloodView.vue'
import NotFound from '@/views/NotFound.vue'

const yearsOptions = ['5years', '30years', '50years']
const typeOptions = ['glb', 'png']
const defaultType = 'glb'

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
        const { years } = to.params
        const { type } = to.query

        // 校验年份参数
        if (!yearsOptions.includes(years)) {
          console.log(
            `Invalid years parameter: ${years}. Valid options are: ${yearsOptions.join(
              ', '
            )}`
          )
          return next('/flood/404')
        }

        // 如果没传 type，自动附加默认类型
        if (!type) {
          return next({
            name: 'flood',
            params: { years },
            query: { type: defaultType }
          })
        }

        // 校验 type 参数是否合法
        if (!typeOptions.includes(type)) {
          console.log(
            `Invalid type parameter: ${type}. Valid options are: ${typeOptions.join(
              ', '
            )}`
          )
          return next('/flood/404')
        }

        // 合法就继续导航
        next()
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
