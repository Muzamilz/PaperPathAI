<template>
  <div class="min-h-screen flex items-center justify-center bg-gray-50">
    <div class="max-w-md w-full text-center">
      <div class="mb-8">
        <h1 class="text-9xl font-bold text-gray-300">404</h1>
      </div>
      
      <div class="mb-8">
        <h2 class="text-2xl font-bold text-gray-900 mb-4">
          {{ $t('notFound.title', 'Page Not Found') }}
        </h2>
        <p class="text-gray-600">
          {{ $t('notFound.description', 'The page you are looking for does not exist.') }}
        </p>
      </div>

      <div class="space-y-4">
        <router-link 
          :to="getLocalizedRoute('home')" 
          class="block w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200"
        >
          {{ $t('notFound.goHome', 'Go Home') }}
        </router-link>
        
        <button 
          @click="goBack" 
          class="block w-full bg-gray-200 text-gray-800 px-6 py-3 rounded-lg font-medium hover:bg-gray-300 transition-colors duration-200"
        >
          {{ $t('common.back', 'Go Back') }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useLanguageStore } from '@/stores/language'

const router = useRouter()
const languageStore = useLanguageStore()

// Methods
const getLocalizedRoute = (routeName, params = {}) => {
  return languageStore.getLocalizedRoute(routeName, params)
}

const goBack = () => {
  router.go(-1)
}
</script>