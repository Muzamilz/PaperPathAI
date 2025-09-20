import { createRouter, createWebHistory } from 'vue-router'
import { useLanguageStore } from '../stores/language'
import { useAuthStore } from '../stores/auth'
import Home from '../views/Home.vue'

const routes = [
  // Redirect root to default language (Arabic)
  {
    path: '/',
    redirect: '/ar'
  },
  // Language-aware routes
  {
    path: '/:lang(en|ar)',
    component: () => import('../views/LanguageWrapper.vue'),
    children: [
      {
        path: '',
        name: 'home',
        component: Home
      },
      {
        path: 'services',
        name: 'services',
        component: () => import('../views/Services.vue')
      },
      {
        path: 'services/:id',
        name: 'ServiceDetail',
        component: () => import('../views/ServiceDetail.vue'),
        props: true
      },
      {
        path: 'portfolio',
        name: 'portfolio',
        component: () => import('../views/Portfolio.vue')
      },
      {
        path: 'portfolio/:id',
        name: 'PortfolioDetail',
        component: () => import('../views/PortfolioDetail.vue'),
        props: true
      },
      {
        path: 'contact',
        name: 'contact',
        component: () => import('../views/Contact.vue')
      },
      {
        path: 'request/:serviceId?',
        name: 'ServiceRequest',
        component: () => import('../views/ServiceRequest.vue'),
        props: true
      },
      // Admin login route
      {
        path: 'admin/login',
        name: 'AdminLogin',
        component: () => import('../views/admin/Login.vue'),
        meta: { requiresGuest: true }
      },
      // Admin routes
      {
        path: 'admin',
        name: 'AdminLayout',
        component: () => import('../views/admin/AdminLayout.vue'),
        meta: { requiresAuth: true, requiresAdmin: true },
        children: [
          {
            path: '',
            name: 'AdminDashboard',
            component: () => import('../views/admin/Dashboard.vue')
          },
          {
            path: 'services',
            name: 'AdminServices',
            component: () => import('../views/admin/Services.vue')
          },
          {
            path: 'requests',
            name: 'AdminRequests',
            component: () => import('../views/admin/Requests.vue')
          },
          {
            path: 'portfolio',
            name: 'AdminPortfolio',
            component: () => import('../views/admin/Portfolio.vue')
          }
        ]
      }
    ]
  },
  // Catch all route for 404
  {
    path: '/:pathMatch(.*)*',
    name: 'NotFound',
    component: () => import('../views/NotFound.vue')
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

// Navigation guards
router.beforeEach(async (to, from, next) => {
  const languageStore = useLanguageStore()
  const authStore = useAuthStore()
  
  // Extract language from route params
  const lang = to.params.lang
  
  if (lang && ['en', 'ar'].includes(lang)) {
    // Set the language in the store
    languageStore.setLanguage(lang)
  }
  
  // Check authentication requirements
  if (to.meta.requiresAuth) {
    // Check if user is authenticated
    const isAuthenticated = await authStore.checkAuth()
    
    if (!isAuthenticated) {
      // Redirect to login with return URL
      next({
        name: 'AdminLogin',
        params: { lang: lang || 'en' },
        query: { redirect: to.fullPath }
      })
      return
    }
    
    // Check admin role requirement
    if (to.meta.requiresAdmin && !authStore.isAdmin) {
      // Redirect to home if not admin
      next({
        name: 'home',
        params: { lang: lang || 'en' }
      })
      return
    }
  }
  
  // Redirect authenticated users away from login
  if (to.meta.requiresGuest && authStore.isAuthenticated) {
    next({
      name: 'AdminDashboard',
      params: { lang: lang || 'en' }
    })
    return
  }
  
  next()
})

export default router