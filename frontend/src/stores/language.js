import { defineStore } from 'pinia'
import { ref, computed, watch } from 'vue'

export const useLanguageStore = defineStore('language', () => {
  // Initialize from localStorage or default to Arabic
  const savedLanguage = localStorage.getItem('language') || 'ar'
  const currentLanguage = ref(savedLanguage)
  
  const direction = computed(() => currentLanguage.value === 'ar' ? 'rtl' : 'ltr')
  const isRTL = computed(() => currentLanguage.value === 'ar')
  const fontFamily = computed(() => 
    currentLanguage.value === 'ar' ? 'font-arabic' : 'font-english'
  )

  const setLanguage = (lang) => {
    if (!['en', 'ar'].includes(lang)) {
      console.warn(`Unsupported language: ${lang}`)
      return
    }
    
    currentLanguage.value = lang
    
    // Update document attributes
    document.documentElement.dir = direction.value
    document.documentElement.lang = lang
    
    // Update body class for direction and font family
    document.body.classList.remove('rtl', 'ltr', 'font-arabic', 'font-english')
    document.body.classList.add(direction.value, fontFamily.value)
    
    // Save to localStorage
    localStorage.setItem('language', lang)
    
    // Update i18n locale if available
    if (window.$i18n) {
      window.$i18n.locale.value = lang
    }
  }

  const toggleLanguage = () => {
    const newLang = currentLanguage.value === 'en' ? 'ar' : 'en'
    setLanguage(newLang)
  }

  const getLocalizedRoute = (routeName, params = {}) => {
    // Map route names to their paths
    const routePaths = {
      'home': '',
      'services': 'services',
      'portfolio': 'portfolio',
      'contact': 'contact',
      'ServiceDetail': `services/${params.id || ':id'}`,
      'PortfolioDetail': `portfolio/${params.id || ':id'}`,
      'ServiceRequest': `request${params.serviceId ? `/${params.serviceId}` : ''}`,
      'admin': 'admin',
      'AdminDashboard': 'admin',
      'AdminServices': 'admin/services',
      'AdminRequests': 'admin/requests',
      'AdminPortfolio': 'admin/portfolio'
    }

    const basePath = `/${currentLanguage.value}`
    const routePath = routePaths[routeName]
    
    // Handle special cases with parameters
    if (routeName === 'ServiceDetail' && params.id) {
      return `${basePath}/services/${params.id}`
    }
    if (routeName === 'PortfolioDetail' && params.id) {
      return `${basePath}/portfolio/${params.id}`
    }
    if (routeName === 'ServiceRequest' && params.serviceId) {
      return `${basePath}/request/${params.serviceId}`
    }
    
    // For home route, return just the base path
    if (routeName === 'home') {
      return basePath
    }
    
    // For other routes, append the route path if it exists
    return routePath ? `${basePath}/${routePath}` : `${basePath}/${routeName}`
  }

  // Watch for language changes and update document
  watch(currentLanguage, (newLang) => {
    document.documentElement.dir = direction.value
    document.documentElement.lang = newLang
  }, { immediate: true })

  // Initialize document on store creation
  if (typeof document !== 'undefined') {
    setLanguage(currentLanguage.value)
  }

  return {
    currentLanguage,
    direction,
    isRTL,
    fontFamily,
    setLanguage,
    toggleLanguage,
    getLocalizedRoute
  }
})