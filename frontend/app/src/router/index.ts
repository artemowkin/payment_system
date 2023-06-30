import { createRouter, createWebHistory, routerKey } from 'vue-router'
import { refresh } from '@/api/auth'
import RegistrationView from '@/views/RegistrationView.vue'
import MerchantsView from '@/views/MerchantsView.vue'
import LoginView from '@/views/LoginView.vue'
import TransactionsView from '@/views/TransactionsView.vue'
import ExampleIntegrationView from '@/views/ExampleIntegrationView.vue'
import PaymentView from '@/views/PaymentView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/registration',
      name: 'registration',
      component: RegistrationView,
    },
    {
      path: '/',
      name: 'merchants',
      component: MerchantsView,
    },
    {
      path: '/transactions',
      name: 'transactions',
      component: TransactionsView,
    },
    {
      path: '/login',
      name: 'login',
      component: LoginView,
    },
    {
      path: '/example_integration',
      name: 'example_integration',
      component: ExampleIntegrationView,
    },
    {
      path: '/payment/:key',
      name: 'payment',
      component: PaymentView,
    },
  ]
})

router.beforeEach(async (to, from) => {
  if (to.name === 'login' || to.name === 'registration' || to.name === 'example_integration' || to.name === 'payment') {
    return true
  }

  const token = localStorage.getItem('refreshToken')

  const tokenPair = await refresh(token)

  if (!tokenPair) {
    return { name: 'login' }
  }

  localStorage.setItem('refreshToken', tokenPair.refresh_token)
  localStorage.setItem('accessToken', tokenPair.access_token)
})

export default router
