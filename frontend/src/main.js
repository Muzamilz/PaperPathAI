import { createApp } from 'vue'
import { createPinia } from 'pinia'
import { createI18n } from 'vue-i18n'
import router from './router'
import App from './App.vue'
import './style.css'

// Import translation messages
import en from './locales/en.json'
import ar from './locales/ar.json'

// Get saved language from localStorage or default to Arabic
const savedLanguage = localStorage.getItem('language') || 'ar'

// Create i18n instance
const i18n = createI18n({
  legacy: false,
  locale: savedLanguage,
  fallbackLocale: 'en',
  messages: {
    en,
    ar
  }
})

const app = createApp(App)

// Create Pinia instance
const pinia = createPinia()

app.use(pinia)
app.use(router)
app.use(i18n)

// Initialize language store after mounting
app.mount('#app')

// Ensure i18n and language store are synchronized
import { useLanguageStore } from './stores/language'
const languageStore = useLanguageStore()
i18n.global.locale.value = languageStore.currentLanguage