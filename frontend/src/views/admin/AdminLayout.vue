<template>
  <div class="min-h-screen bg-gray-100 flex" :class="{ 'rtl': isRTL }">
    <!-- Sidebar -->
    <div class="hidden md:flex md:w-64 md:flex-col">
      <div class="flex flex-col flex-grow pt-5 bg-white overflow-y-auto border-r border-gray-200">
        <!-- Logo -->
        <div class="flex items-center flex-shrink-0 px-4 mb-8">
          <router-link :to="getLocalizedRoute('home')" class="flex items-center">
            <img 
              src="/src/paperpath_logo.svg" 
              alt="PaperPath Logo" 
              class="h-8 w-auto object-contain"
            />
            <span class="ml-3 text-lg font-semibold text-gray-900" :class="{ 'mr-3 ml-0': isRTL }">
              {{ $t('admin.dashboard') }}
            </span>
          </router-link>
        </div>

        <!-- Navigation -->
        <nav class="mt-5 flex-1 px-2 space-y-2">
          <router-link
            :to="{ name: 'AdminDashboard', params: { lang: currentLanguage } }"
            class="sidebar-link group animate-fade-in-left animate-stagger-1"
            :class="{ 'active': $route.name === 'AdminDashboard' }"
          >
            <div class="w-8 h-8 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200" 
                 :class="$route.name === 'AdminDashboard' ? 'bg-blue-100' : 'bg-gray-100 group-hover:bg-blue-50'">
              <svg class="w-4 h-4" :class="$route.name === 'AdminDashboard' ? 'text-blue-600' : 'text-gray-600 group-hover:text-blue-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 7v10a2 2 0 002 2h14a2 2 0 002-2V9a2 2 0 00-2-2H5a2 2 0 00-2-2z" />
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 5a2 2 0 012-2h4a2 2 0 012 2v6H8V5z" />
              </svg>
            </div>
            <span class="ml-3" :class="{ 'mr-3 ml-0': isRTL }">{{ $t('admin.dashboard') }}</span>
            <div v-if="$route.name === 'AdminDashboard'" class="ml-auto w-2 h-2 bg-blue-600 rounded-full" :class="{ 'mr-auto ml-0': isRTL }"></div>
          </router-link>

          <router-link
            :to="{ name: 'AdminServices', params: { lang: currentLanguage } }"
            class="sidebar-link group animate-fade-in-left animate-stagger-2"
            :class="{ 'active': $route.name === 'AdminServices' }"
          >
            <div class="w-8 h-8 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200" 
                 :class="$route.name === 'AdminServices' ? 'bg-green-100' : 'bg-gray-100 group-hover:bg-green-50'">
              <svg class="w-4 h-4" :class="$route.name === 'AdminServices' ? 'text-green-600' : 'text-gray-600 group-hover:text-green-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
            <span class="ml-3" :class="{ 'mr-3 ml-0': isRTL }">{{ $t('nav.services') }}</span>
            <div v-if="$route.name === 'AdminServices'" class="ml-auto w-2 h-2 bg-green-600 rounded-full" :class="{ 'mr-auto ml-0': isRTL }"></div>
          </router-link>

          <router-link
            :to="{ name: 'AdminRequests', params: { lang: currentLanguage } }"
            class="sidebar-link group animate-fade-in-left animate-stagger-3"
            :class="{ 'active': $route.name === 'AdminRequests' }"
          >
            <div class="w-8 h-8 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200" 
                 :class="$route.name === 'AdminRequests' ? 'bg-purple-100' : 'bg-gray-100 group-hover:bg-purple-50'">
              <svg class="w-4 h-4" :class="$route.name === 'AdminRequests' ? 'text-purple-600' : 'text-gray-600 group-hover:text-purple-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
              </svg>
            </div>
            <span class="ml-3" :class="{ 'mr-3 ml-0': isRTL }">{{ $t('admin.requests') }}</span>
            <div v-if="$route.name === 'AdminRequests'" class="ml-auto w-2 h-2 bg-purple-600 rounded-full" :class="{ 'mr-auto ml-0': isRTL }"></div>
          </router-link>

          <router-link
            :to="{ name: 'AdminPortfolio', params: { lang: currentLanguage } }"
            class="sidebar-link group animate-fade-in-left animate-stagger-4"
            :class="{ 'active': $route.name === 'AdminPortfolio' }"
          >
            <div class="w-8 h-8 rounded-lg flex items-center justify-center group-hover:scale-110 transition-transform duration-200" 
                 :class="$route.name === 'AdminPortfolio' ? 'bg-orange-100' : 'bg-gray-100 group-hover:bg-orange-50'">
              <svg class="w-4 h-4" :class="$route.name === 'AdminPortfolio' ? 'text-orange-600' : 'text-gray-600 group-hover:text-orange-600'" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
              </svg>
            </div>
            <span class="ml-3" :class="{ 'mr-3 ml-0': isRTL }">{{ $t('admin.portfolio') }}</span>
            <div v-if="$route.name === 'AdminPortfolio'" class="ml-auto w-2 h-2 bg-orange-600 rounded-full" :class="{ 'mr-auto ml-0': isRTL }"></div>
          </router-link>
        </nav>

        <!-- User Menu -->
        <div class="flex-shrink-0 flex border-t border-gray-200 p-4">
          <div class="flex-shrink-0 w-full group block">
            <div class="flex items-center justify-between">
              <div class="flex items-center">
                <div class="w-8 h-8 bg-blue-100 rounded-full flex items-center justify-center">
                  <svg class="w-4 h-4 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
                  </svg>
                </div>
                <div class="ml-3" :class="{ 'mr-3 ml-0': isRTL }">
                  <p class="text-sm font-medium text-gray-700">
                    {{ authStore.user?.username || 'Admin' }}
                  </p>
                  <p class="text-xs font-medium text-gray-500">
                    {{ $t('admin.dashboard') }}
                  </p>
                </div>
              </div>
              
              <!-- Language & Logout -->
              <div class="flex items-center space-x-2" :class="{ 'space-x-reverse': isRTL }">
                <select
                  v-model="currentLanguage"
                  @change="changeLanguage"
                  class="text-xs border border-gray-300 rounded px-2 py-1 focus:outline-none focus:ring-1 focus:ring-blue-500"
                >
                  <option value="en">EN</option>
                  <option value="ar">AR</option>
                </select>
                
                <button
                  @click="handleLogout"
                  class="text-gray-400 hover:text-gray-600 transition-colors duration-200"
                  :title="$t('admin.logout')"
                >
                  <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                  </svg>
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Mobile sidebar -->
    <div v-if="mobileMenuOpen" class="fixed inset-0 flex z-40 md:hidden">
      <div class="fixed inset-0 bg-gray-600 bg-opacity-75" @click="mobileMenuOpen = false"></div>
      <div class="relative flex-1 flex flex-col max-w-xs w-full bg-white">
        <div class="absolute top-0 right-0 -mr-12 pt-2" :class="{ 'right-auto left-0 -ml-12': isRTL }">
          <button
            @click="mobileMenuOpen = false"
            class="ml-1 flex items-center justify-center h-10 w-10 rounded-full focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
            :class="{ 'mr-1 ml-0': isRTL }"
          >
            <svg class="h-6 w-6 text-white" stroke="currentColor" fill="none" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>
        
        <div class="flex-1 h-0 pt-5 pb-4 overflow-y-auto">
          <div class="flex-shrink-0 flex items-center px-4 mb-8">
            <img 
              src="/src/paperpath_logo.svg" 
              alt="PaperPath Logo" 
              class="h-8 w-auto object-contain"
            />
            <span class="ml-3 text-lg font-semibold text-gray-900" :class="{ 'mr-3 ml-0': isRTL }">
              {{ $t('admin.dashboard') }}
            </span>
          </div>
          
          <nav class="mt-5 px-2 space-y-1">
            <router-link
              :to="{ name: 'AdminDashboard', params: { lang: currentLanguage } }"
              class="mobile-sidebar-link group"
              :class="{ 'active': $route.name === 'AdminDashboard' }"
              @click="mobileMenuOpen = false"
            >
              {{ $t('admin.dashboard') }}
            </router-link>
            <router-link
              :to="{ name: 'AdminServices', params: { lang: currentLanguage } }"
              class="mobile-sidebar-link group"
              :class="{ 'active': $route.name === 'AdminServices' }"
              @click="mobileMenuOpen = false"
            >
              {{ $t('nav.services') }}
            </router-link>
            <router-link
              :to="{ name: 'AdminRequests', params: { lang: currentLanguage } }"
              class="mobile-sidebar-link group"
              :class="{ 'active': $route.name === 'AdminRequests' }"
              @click="mobileMenuOpen = false"
            >
              {{ $t('admin.requests') }}
            </router-link>
            <router-link
              :to="{ name: 'AdminPortfolio', params: { lang: currentLanguage } }"
              class="mobile-sidebar-link group"
              :class="{ 'active': $route.name === 'AdminPortfolio' }"
              @click="mobileMenuOpen = false"
            >
              {{ $t('admin.portfolio') }}
            </router-link>
          </nav>
        </div>
        
        <div class="flex-shrink-0 flex border-t border-gray-200 p-4">
          <button
            @click="handleLogout"
            class="flex-shrink-0 w-full group block text-left"
          >
            <div class="flex items-center">
              <div class="w-8 h-8 bg-red-100 rounded-full flex items-center justify-center">
                <svg class="w-4 h-4 text-red-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1" />
                </svg>
              </div>
              <div class="ml-3" :class="{ 'mr-3 ml-0': isRTL }">
                <p class="text-sm font-medium text-gray-700">{{ $t('admin.logout') }}</p>
              </div>
            </div>
          </button>
        </div>
      </div>
    </div>

    <!-- Main content -->
    <div class="flex flex-col w-0 flex-1 overflow-hidden">
      <!-- Top bar for mobile -->
      <div class="md:hidden">
        <div class="relative z-10 flex-shrink-0 flex h-16 bg-white shadow">
          <button
            @click="mobileMenuOpen = true"
            class="px-4 border-r border-gray-200 text-gray-500 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500 md:hidden"
          >
            <svg class="h-6 w-6" stroke="currentColor" fill="none" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 12h16M4 18h16" />
            </svg>
          </button>
          <div class="flex-1 px-4 flex justify-between">
            <div class="flex-1 flex">
              <div class="w-full flex md:ml-0">
                <div class="flex items-center">
                  <h1 class="text-lg font-semibold text-gray-900">{{ $t('admin.dashboard') }}</h1>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Main content area -->
      <main class="flex-1 relative overflow-y-auto focus:outline-none">
        <div class="py-6">
          <div class="max-w-7xl mx-auto px-4 sm:px-6 md:px-8">
            <router-view />
          </div>
        </div>
      </main>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useLanguageStore } from '@/stores/language'

const router = useRouter()
const authStore = useAuthStore()
const languageStore = useLanguageStore()

// State
const mobileMenuOpen = ref(false)

// Computed
const currentLanguage = computed({
  get: () => languageStore.currentLanguage,
  set: (value) => languageStore.setLanguage(value)
})

const isRTL = computed(() => languageStore.direction === 'rtl')

// Methods
const getLocalizedRoute = (routeName, params = {}) => {
  return languageStore.getLocalizedRoute(routeName, params)
}

const changeLanguage = (event) => {
  const newLang = event.target.value
  languageStore.setLanguage(newLang)
  
  // Update the current route with new language
  const currentRoute = router.currentRoute.value
  const newRoute = {
    ...currentRoute,
    params: {
      ...currentRoute.params,
      lang: newLang
    }
  }
  router.push(newRoute)
}

const handleLogout = async () => {
  await authStore.logout()
  router.push({
    name: 'Home',
    params: { lang: currentLanguage.value }
  })
}
</script>

<style scoped>
.sidebar-link {
  @apply text-gray-600 hover:bg-gray-50 hover:text-gray-900 flex items-center px-2 py-2 text-sm font-medium rounded-md transition-colors duration-200;
}

.sidebar-link.active {
  @apply bg-blue-100 text-blue-700;
}

.mobile-sidebar-link {
  @apply text-gray-600 hover:bg-gray-50 hover:text-gray-900 flex items-center px-2 py-2 text-base font-medium rounded-md transition-colors duration-200;
}

.mobile-sidebar-link.active {
  @apply bg-blue-100 text-blue-700;
}

/* RTL Support */
.rtl .sidebar-link {
  @apply flex-row-reverse;
}

.rtl .mobile-sidebar-link {
  @apply flex-row-reverse;
}
</style>