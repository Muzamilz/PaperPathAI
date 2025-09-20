<template>
  <header class="bg-white/95 backdrop-blur-md shadow-lg border-b border-gray-200 sticky top-0 z-50">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
      <div class="flex justify-between items-center h-16">
        <!-- Logo and Brand -->
        <div class="flex items-center">
          <router-link 
            :to="getLocalizedRoute('home')" 
            class="flex items-center"
          >
            <img 
              src="/src/paperpath_logo.svg" 
              alt="PaperPath Logo" 
              class="h-10 w-auto object-contain"
            />
          </router-link>
        </div>

        <!-- Desktop Navigation -->
        <nav class="hidden md:flex items-center space-x-8 rtl:space-x-reverse">
          <router-link
            v-for="item in navigationItems"
            :key="item.name"
            :to="getLocalizedRoute(item.route)"
            class="text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
            :class="{ 'text-blue-600 bg-blue-50': isActiveRoute(item.route) }"
          >
            {{ $t(`nav.${item.name}`) }}
          </router-link>
        </nav>

        <!-- Language Selector and Mobile Menu Button -->
        <div class="flex items-center space-x-4 rtl:space-x-reverse">
          <!-- Language Selector -->
          <div class="relative">
            <button
              @click="toggleLanguageDropdown"
              class="flex items-center space-x-2 rtl:space-x-reverse text-gray-700 hover:text-blue-600 px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200"
              :aria-expanded="showLanguageDropdown"
              aria-haspopup="true"
            >
              <span>{{ currentLanguage.toUpperCase() }}</span>
              <svg 
                class="w-4 h-4 transition-transform duration-200"
                :class="{ 'rotate-180': showLanguageDropdown }"
                fill="none" 
                stroke="currentColor" 
                viewBox="0 0 24 24"
              >
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
              </svg>
            </button>
            
            <!-- Language Dropdown -->
            <transition
              enter-active-class="transition ease-out duration-100"
              enter-from-class="transform opacity-0 scale-95"
              enter-to-class="transform opacity-100 scale-100"
              leave-active-class="transition ease-in duration-75"
              leave-from-class="transform opacity-100 scale-100"
              leave-to-class="transform opacity-0 scale-95"
            >
              <div
                v-if="showLanguageDropdown"
                class="absolute right-0 rtl:right-auto rtl:left-0 mt-2 w-32 bg-white rounded-md shadow-lg ring-1 ring-black ring-opacity-5 z-50"
              >
                <div class="py-1">
                  <button
                    v-for="lang in availableLanguages"
                    :key="lang.code"
                    @click="changeLanguage(lang.code)"
                    class="flex items-center w-full px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 transition-colors duration-200"
                    :class="{ 'bg-blue-50 text-blue-600': currentLanguage === lang.code }"
                  >
                    <span class="mr-3 rtl:mr-0 rtl:ml-3">{{ lang.flag }}</span>
                    {{ lang.name }}
                  </button>
                </div>
              </div>
            </transition>
          </div>

          <!-- Mobile menu button -->
          <button
            @click="toggleMobileMenu"
            class="md:hidden inline-flex items-center justify-center p-2 rounded-md text-gray-700 hover:text-blue-600 hover:bg-gray-100 transition-colors duration-200"
            :aria-expanded="showMobileMenu"
            aria-label="Toggle navigation menu"
          >
            <svg 
              class="w-6 h-6" 
              :class="{ 'hidden': showMobileMenu, 'block': !showMobileMenu }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
            <svg 
              class="w-6 h-6" 
              :class="{ 'block': showMobileMenu, 'hidden': !showMobileMenu }"
              fill="none" 
              stroke="currentColor" 
              viewBox="0 0 24 24"
            >
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Mobile Navigation Menu -->
      <transition
        enter-active-class="transition ease-out duration-200"
        enter-from-class="transform opacity-0 scale-95"
        enter-to-class="transform opacity-100 scale-100"
        leave-active-class="transition ease-in duration-100"
        leave-from-class="transform opacity-100 scale-100"
        leave-to-class="transform opacity-0 scale-95"
      >
        <div v-if="showMobileMenu" class="md:hidden">
          <div class="px-2 pt-2 pb-3 space-y-1 bg-gray-50 border-t border-gray-200">
            <router-link
              v-for="item in navigationItems"
              :key="item.name"
              :to="getLocalizedRoute(item.route)"
              @click="closeMobileMenu"
              class="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-blue-600 hover:bg-white transition-colors duration-200"
              :class="{ 'text-blue-600 bg-white': isActiveRoute(item.route) }"
            >
              {{ $t(`nav.${item.name}`) }}
            </router-link>
          </div>
        </div>
      </transition>
    </div>
  </header>
</template>

<script setup>
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useLanguageStore } from '@/stores/language'

const route = useRoute()
const router = useRouter()
const { locale } = useI18n()
const languageStore = useLanguageStore()

// Reactive state
const showMobileMenu = ref(false)
const showLanguageDropdown = ref(false)

// Computed properties
const currentLanguage = computed(() => languageStore.currentLanguage)

const navigationItems = [
  { name: 'home', route: 'home' },
  { name: 'services', route: 'services' },
  { name: 'portfolio', route: 'portfolio' },
  { name: 'contact', route: 'contact' }
]

const availableLanguages = [
  { code: 'en', name: 'English', flag: '🇺🇸' },
  { code: 'ar', name: 'العربية', flag: '🇸🇦' }
]

// Methods
const toggleMobileMenu = () => {
  showMobileMenu.value = !showMobileMenu.value
  showLanguageDropdown.value = false
}

const closeMobileMenu = () => {
  showMobileMenu.value = false
}

const toggleLanguageDropdown = () => {
  showLanguageDropdown.value = !showLanguageDropdown.value
  showMobileMenu.value = false
}

const changeLanguage = (langCode) => {
  languageStore.setLanguage(langCode)
  locale.value = langCode
  showLanguageDropdown.value = false
  
  // Navigate to the same route with new language
  const currentRouteName = route.name?.toString().replace(/^(en|ar)-/, '') || 'home'
  router.push(getLocalizedRoute(currentRouteName, route.params))
}

const getLocalizedRoute = (routeName, params = {}) => {
  return languageStore.getLocalizedRoute(routeName, params)
}

const isActiveRoute = (routeName) => {
  const currentRouteName = route.name?.toString().replace(/^(en|ar)-/, '')
  return currentRouteName === routeName
}

// Close dropdowns when clicking outside
const handleClickOutside = (event) => {
  if (!event.target.closest('.relative')) {
    showLanguageDropdown.value = false
  }
}

onMounted(() => {
  document.addEventListener('click', handleClickOutside)
})

onUnmounted(() => {
  document.removeEventListener('click', handleClickOutside)
})
</script>

<style scoped>
/* Additional styles for RTL support */
.rtl .space-x-2 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}

.rtl .space-x-4 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}

.rtl .space-x-8 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}
</style>