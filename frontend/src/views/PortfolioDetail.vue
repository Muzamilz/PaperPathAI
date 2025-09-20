<template>
  <div class="container mx-auto px-4 py-8">
    <div class="max-w-4xl mx-auto">
      <!-- Breadcrumb -->
      <nav class="mb-6">
        <ol class="flex items-center space-x-2 rtl:space-x-reverse text-sm text-gray-600">
          <li>
            <router-link :to="getLocalizedRoute('home')" class="hover:text-blue-600">
              {{ $t('nav.home') }}
            </router-link>
          </li>
          <li class="flex items-center">
            <svg class="w-4 h-4 mx-2 rtl:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <router-link :to="getLocalizedRoute('portfolio')" class="hover:text-blue-600">
              {{ $t('nav.portfolio') }}
            </router-link>
          </li>
          <li class="flex items-center">
            <svg class="w-4 h-4 mx-2 rtl:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <span class="text-gray-900">{{ portfolioItem?.title || 'Portfolio Detail' }}</span>
          </li>
        </ol>
      </nav>

      <!-- Loading State -->
      <div v-if="loading" class="flex justify-center items-center py-12">
        <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
      </div>

      <!-- Error State -->
      <div v-else-if="error" class="text-center py-12">
        <div class="text-red-600 mb-4">{{ $t('common.error') }}</div>
        <button @click="fetchPortfolioItem" class="btn btn-primary">
          {{ $t('common.retry') }}
        </button>
      </div>

      <!-- Portfolio Item Content -->
      <div v-else-if="portfolioItem" class="bg-white rounded-lg shadow-lg overflow-hidden">
        <!-- Portfolio Header -->
        <div class="p-6 border-b border-gray-200">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ portfolioItem.title }}</h1>
          <div class="flex flex-wrap items-center gap-4 text-sm text-gray-600">
            <span class="flex items-center">
              <svg class="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              {{ portfolioItem.service_category?.name }}
            </span>
            <span class="flex items-center">
              <svg class="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {{ $t('portfolio.completedOn') }}: {{ formatDate(portfolioItem.completion_date) }}
            </span>
          </div>
        </div>

        <!-- Portfolio Content -->
        <div class="p-6">
          <!-- Image -->
          <div v-if="portfolioItem.image" class="mb-8">
            <img 
              :src="portfolioItem.image" 
              :alt="portfolioItem.title"
              class="w-full h-96 object-cover rounded-lg shadow-md"
            />
          </div>

          <!-- Description -->
          <div class="prose max-w-none mb-8">
            <h2 class="text-xl font-semibold mb-4">Project Description</h2>
            <div v-html="portfolioItem.description"></div>
          </div>

          <!-- Technologies Used -->
          <div v-if="portfolioItem.technologies_used && portfolioItem.technologies_used.length" class="mb-8">
            <h3 class="text-lg font-semibold mb-4">{{ $t('portfolio.technologies') }}</h3>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="tech in portfolioItem.technologies_used" 
                :key="tech"
                class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
              >
                {{ tech }}
              </span>
            </div>
          </div>

          <!-- Client Type -->
          <div class="bg-gray-50 rounded-lg p-4">
            <h3 class="text-lg font-semibold mb-2">Client Type</h3>
            <p class="text-gray-700">{{ portfolioItem.client_type }}</p>
          </div>
        </div>
      </div>

      <!-- Not Found -->
      <div v-else class="text-center py-12">
        <h1 class="text-2xl font-bold text-gray-900 mb-4">Portfolio Item Not Found</h1>
        <p class="text-gray-600 mb-6">The portfolio item you're looking for doesn't exist.</p>
        <router-link :to="getLocalizedRoute('portfolio')" class="btn btn-primary">
          {{ $t('nav.portfolio') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { usePortfolioStore } from '@/stores/portfolio'
import { useLanguageStore } from '@/stores/language'

const route = useRoute()
const portfolioStore = usePortfolioStore()
const languageStore = useLanguageStore()

// Props
const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  }
})

// Reactive state
const portfolioItem = ref(null)
const loading = ref(false)
const error = ref(null)

// Methods
const getLocalizedRoute = (routeName, params = {}) => {
  return languageStore.getLocalizedRoute(routeName, params)
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString(languageStore.currentLanguage === 'ar' ? 'ar-SA' : 'en-US')
}

const fetchPortfolioItem = async () => {
  loading.value = true
  error.value = null
  
  try {
    portfolioItem.value = await portfolioStore.getPortfolioItemDetails(props.id)
  } catch (err) {
    error.value = err.message
    console.error('Error fetching portfolio item:', err)
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  fetchPortfolioItem()
})
</script>

<style scoped>
.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors duration-200;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700;
}

.prose h2 {
  @apply text-xl font-semibold mb-4 text-gray-900;
}

.prose p {
  @apply mb-4 text-gray-700 leading-relaxed;
}
</style>