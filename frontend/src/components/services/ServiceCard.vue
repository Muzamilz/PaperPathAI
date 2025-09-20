<template>
  <div class="bg-white rounded-lg shadow-md hover:shadow-lg transition-shadow duration-300 overflow-hidden">
    <!-- Service Header -->
    <div class="p-6">
      <!-- Category Badge -->
      <div class="flex items-center justify-between mb-3">
        <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
          {{ service.category?.name || 'General' }}
        </span>
        <div v-if="service.is_featured" class="text-yellow-500">
          <svg class="w-5 h-5" fill="currentColor" viewBox="0 0 20 20">
            <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
          </svg>
        </div>
      </div>

      <!-- Service Title -->
      <h3 class="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
        {{ service.title }}
      </h3>

      <!-- Service Description -->
      <p class="text-gray-600 text-sm mb-4 line-clamp-3">
        {{ service.short_description }}
      </p>

      <!-- Service Details -->
      <div class="space-y-2 mb-4">
        <!-- Price Range -->
        <div class="flex items-center text-sm">
          <svg class="w-4 h-4 text-gray-400 mr-2 rtl:mr-0 rtl:ml-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1" />
          </svg>
          <span class="text-gray-700">
            <span class="font-medium">{{ $t('services.priceRange') }}:</span>
            {{ service.price_range }}
          </span>
        </div>

        <!-- Delivery Time -->
        <div class="flex items-center text-sm">
          <svg class="w-4 h-4 text-gray-400 mr-2 rtl:mr-0 rtl:ml-2 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
          </svg>
          <span class="text-gray-700">
            <span class="font-medium">{{ $t('services.deliveryTime') }}:</span>
            {{ service.delivery_time }}
          </span>
        </div>
      </div>

      <!-- Features Preview -->
      <div v-if="service.features && service.features.length" class="mb-4">
        <div class="flex flex-wrap gap-1">
          <span 
            v-for="(feature, index) in service.features.slice(0, 3)" 
            :key="index"
            class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800"
          >
            {{ feature }}
          </span>
          <span 
            v-if="service.features.length > 3"
            class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-600"
          >
            +{{ service.features.length - 3 }} {{ $t('common.more', 'more') }}
          </span>
        </div>
      </div>
    </div>

    <!-- Action Buttons -->
    <div class="px-6 py-4 bg-gray-50 border-t border-gray-200">
      <div class="flex space-x-3 rtl:space-x-reverse">
        <router-link
          :to="getLocalizedRoute('ServiceDetail', { id: service.id })"
          class="flex-1 bg-white text-gray-700 border border-gray-300 px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-50 transition-colors duration-200 text-center"
        >
          {{ $t('services.viewDetails') }}
        </router-link>
        <router-link
          :to="getLocalizedRoute('ServiceRequest', { serviceId: service.id })"
          class="flex-1 bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors duration-200 text-center"
        >
          {{ $t('services.requestService') }}
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { useLanguageStore } from '@/stores/language'

const languageStore = useLanguageStore()

// Props
const props = defineProps({
  service: {
    type: Object,
    required: true
  }
})

// Methods
const getLocalizedRoute = (routeName, params = {}) => {
  return languageStore.getLocalizedRoute(routeName, params)
}
</script>

<style scoped>
/* Line clamp utilities */
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

/* RTL support for flex items */
.rtl .space-x-3 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}

.rtl .space-x-reverse > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}
</style>