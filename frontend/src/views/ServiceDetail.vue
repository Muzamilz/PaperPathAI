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
            <router-link :to="getLocalizedRoute('services')" class="hover:text-blue-600">
              {{ $t('nav.services') }}
            </router-link>
          </li>
          <li class="flex items-center">
            <svg class="w-4 h-4 mx-2 rtl:rotate-180" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
            </svg>
            <span class="text-gray-900">{{ service?.title || 'Service Detail' }}</span>
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
        <button @click="fetchService" class="btn btn-primary">
          {{ $t('common.retry') }}
        </button>
      </div>

      <!-- Service Detail Content -->
      <div v-else-if="service" class="bg-white rounded-lg shadow-lg overflow-hidden">
        <!-- Service Header -->
        <div class="p-6 border-b border-gray-200">
          <h1 class="text-3xl font-bold text-gray-900 mb-2">{{ service.title }}</h1>
          <p class="text-gray-600">{{ service.short_description }}</p>
        </div>

        <!-- Service Content -->
        <div class="p-6">
          <div class="grid grid-cols-1 lg:grid-cols-3 gap-8">
            <!-- Main Content -->
            <div class="lg:col-span-2">
              <div class="prose max-w-none">
                <h2 class="text-xl font-semibold mb-4">{{ $t('services.description') }}</h2>
                <div v-html="service.description"></div>
              </div>

              <!-- Features -->
              <div v-if="service.features && service.features.length" class="mt-8">
                <h3 class="text-lg font-semibold mb-4">{{ $t('services.features') }}</h3>
                <ul class="space-y-2">
                  <li v-for="feature in service.features" :key="feature" class="flex items-start">
                    <svg class="w-5 h-5 text-green-500 mt-0.5 mr-2 rtl:mr-0 rtl:ml-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7" />
                    </svg>
                    <span>{{ feature }}</span>
                  </li>
                </ul>
              </div>
            </div>

            <!-- Sidebar -->
            <div class="lg:col-span-1">
              <div class="bg-gray-50 rounded-lg p-6 sticky top-6">
                <!-- Pricing -->
                <div class="mb-6">
                  <h3 class="text-lg font-semibold mb-2">{{ $t('services.priceRange') }}</h3>
                  <p class="text-2xl font-bold text-blue-600">{{ service.price_range }}</p>
                </div>

                <!-- Delivery Time -->
                <div class="mb-6">
                  <h3 class="text-lg font-semibold mb-2">{{ $t('services.deliveryTime') }}</h3>
                  <p class="text-gray-700">{{ service.delivery_time }}</p>
                </div>

                <!-- Action Button -->
                <router-link
                  :to="getLocalizedRoute('ServiceRequest', { serviceId: service.id })"
                  class="w-full bg-blue-600 text-white px-6 py-3 rounded-lg font-medium hover:bg-blue-700 transition-colors duration-200 text-center block"
                >
                  {{ $t('services.requestService') }}
                </router-link>
              </div>
            </div>
          </div>
        </div>
      </div>

      <!-- Not Found -->
      <div v-else class="text-center py-12">
        <h1 class="text-2xl font-bold text-gray-900 mb-4">Service Not Found</h1>
        <p class="text-gray-600 mb-6">The service you're looking for doesn't exist.</p>
        <router-link :to="getLocalizedRoute('services')" class="btn btn-primary">
          {{ $t('nav.services') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useServicesStore } from '@/stores/services'
import { useLanguageStore } from '@/stores/language'

const route = useRoute()
const servicesStore = useServicesStore()
const languageStore = useLanguageStore()

// Props
const props = defineProps({
  id: {
    type: [String, Number],
    required: true
  }
})

// Reactive state
const service = ref(null)
const loading = ref(false)
const error = ref(null)

// Methods
const getLocalizedRoute = (routeName, params = {}) => {
  return languageStore.getLocalizedRoute(routeName, params)
}

const fetchService = async () => {
  loading.value = true
  error.value = null
  
  try {
    service.value = await servicesStore.getServiceDetails(props.id)
  } catch (err) {
    error.value = err.message
    console.error('Error fetching service:', err)
  } finally {
    loading.value = false
  }
}

// Lifecycle
onMounted(() => {
  fetchService()
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