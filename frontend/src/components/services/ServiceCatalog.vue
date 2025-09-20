<template>
  <div class="space-y-6">
    <!-- Header Section -->
    <div class="text-center">
      <h1 class="text-3xl font-bold text-gray-900 mb-4">{{ $t('services.title') }}</h1>
      <p class="text-lg text-gray-600 max-w-2xl mx-auto">{{ $t('services.description') }}</p>
    </div>

    <!-- Filters and Search -->
    <div class="bg-white rounded-lg shadow-sm border border-gray-200 p-6">
      <div class="flex flex-col lg:flex-row gap-4 items-center">
        <!-- Search Input -->
        <div class="flex-1 w-full lg:w-auto">
          <div class="relative">
            <div class="absolute inset-y-0 left-0 rtl:left-auto rtl:right-0 pl-3 rtl:pl-0 rtl:pr-3 flex items-center pointer-events-none">
              <svg class="h-5 w-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
              </svg>
            </div>
            <input
              v-model="searchQuery"
              type="text"
              :placeholder="$t('common.search') + ' ' + $t('nav.services').toLowerCase() + '...'"
              class="block w-full pl-10 rtl:pl-3 rtl:pr-10 pr-3 py-2 border border-gray-300 rounded-md leading-5 bg-white placeholder-gray-500 focus:outline-none focus:placeholder-gray-400 focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
        </div>

        <!-- Category Filter -->
        <div class="w-full lg:w-auto">
          <select
            v-model="selectedCategory"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="">{{ $t('common.all') }} {{ $t('services.categories', 'Categories') }}</option>
            <option 
              v-for="category in categories" 
              :key="category?.id || category" 
              :value="category?.id"
            >
              {{ category?.name }}
            </option>
          </select>
        </div>

        <!-- Sort Options -->
        <div class="w-full lg:w-auto">
          <select
            v-model="sortBy"
            class="block w-full px-3 py-2 border border-gray-300 rounded-md bg-white focus:outline-none focus:ring-1 focus:ring-blue-500 focus:border-blue-500"
          >
            <option value="title">{{ $t('services.sortBy.title', 'Sort by Title') }}</option>
            <option value="price">{{ $t('services.sortBy.price', 'Sort by Price') }}</option>
            <option value="delivery">{{ $t('services.sortBy.delivery', 'Sort by Delivery Time') }}</option>
            <option value="featured">{{ $t('services.sortBy.featured', 'Featured First') }}</option>
          </select>
        </div>

        <!-- View Toggle -->
        <div class="flex rounded-md shadow-sm">
          <button
            @click="viewMode = 'grid'"
            :class="[
              'px-3 py-2 text-sm font-medium rounded-l-md border transition-colors duration-200',
              viewMode === 'grid' 
                ? 'bg-blue-600 text-white border-blue-600' 
                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
            ]"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z" />
            </svg>
          </button>
          <button
            @click="viewMode = 'list'"
            :class="[
              'px-3 py-2 text-sm font-medium rounded-r-md border-t border-r border-b transition-colors duration-200',
              viewMode === 'list' 
                ? 'bg-blue-600 text-white border-blue-600' 
                : 'bg-white text-gray-700 border-gray-300 hover:bg-gray-50'
            ]"
          >
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 6h16M4 10h16M4 14h16M4 18h16" />
            </svg>
          </button>
        </div>
      </div>

      <!-- Active Filters -->
      <div v-if="hasActiveFilters" class="mt-4 flex flex-wrap gap-2">
        <span class="text-sm text-gray-600">{{ $t('common.activeFilters', 'Active filters') }}:</span>
        <span 
          v-if="searchQuery"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
        >
          {{ $t('common.search') }}: "{{ searchQuery }}"
          <button @click="searchQuery = ''" class="ml-1 rtl:ml-0 rtl:mr-1">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </span>
        <span 
          v-if="selectedCategory"
          class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800"
        >
          {{ getCategoryName(selectedCategory) }}
          <button @click="selectedCategory = ''" class="ml-1 rtl:ml-0 rtl:mr-1">
            <svg class="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </span>
        <button 
          @click="clearAllFilters"
          class="text-xs text-blue-600 hover:text-blue-800 underline"
        >
          {{ $t('common.clearAll', 'Clear all') }}
        </button>
      </div>
    </div>

    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-600 mb-4">{{ error }}</div>
      <button @click="fetchServices" class="btn btn-primary">
        {{ $t('common.retry') }}
      </button>
    </div>

    <!-- Services Grid/List -->
    <div v-else-if="filteredServices.length">
      <!-- Results Count -->
      <div class="text-sm text-gray-600 mb-4">
        {{ $t('services.resultsCount', 'Showing {count} services', { count: filteredServices.length }) }}
      </div>

      <!-- Grid View -->
      <div 
        v-if="viewMode === 'grid'"
        class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6"
      >
        <ServiceCard 
          v-for="service in paginatedServices" 
          :key="service.id" 
          :service="service" 
        />
      </div>

      <!-- List View -->
      <div v-else class="space-y-4">
        <div 
          v-for="service in paginatedServices" 
          :key="service.id"
          class="bg-white rounded-lg shadow-sm border border-gray-200 p-6"
        >
          <div class="flex flex-col lg:flex-row lg:items-center lg:justify-between">
            <div class="flex-1">
              <div class="flex items-center mb-2">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 mr-3 rtl:mr-0 rtl:ml-3">
                  {{ service.category?.name || 'General' }}
                </span>
                <div v-if="service.is_featured" class="text-yellow-500">
                  <svg class="w-4 h-4" fill="currentColor" viewBox="0 0 20 20">
                    <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                  </svg>
                </div>
              </div>
              <h3 class="text-lg font-semibold text-gray-900 mb-2">{{ service.title }}</h3>
              <p class="text-gray-600 mb-3">{{ service.short_description }}</p>
              <div class="flex flex-wrap gap-4 text-sm text-gray-600">
                <span>{{ $t('services.priceRange') }}: {{ service.price_range }}</span>
                <span>{{ $t('services.deliveryTime') }}: {{ service.delivery_time }}</span>
              </div>
            </div>
            <div class="mt-4 lg:mt-0 lg:ml-6 rtl:lg:ml-0 rtl:lg:mr-6 flex space-x-3 rtl:space-x-reverse">
              <router-link
                :to="getLocalizedRoute('ServiceDetail', { id: service.id })"
                class="bg-white text-gray-700 border border-gray-300 px-4 py-2 rounded-md text-sm font-medium hover:bg-gray-50 transition-colors duration-200"
              >
                {{ $t('services.viewDetails') }}
              </router-link>
              <router-link
                :to="getLocalizedRoute('ServiceRequest', { serviceId: service.id })"
                class="bg-blue-600 text-white px-4 py-2 rounded-md text-sm font-medium hover:bg-blue-700 transition-colors duration-200"
              >
                {{ $t('services.requestService') }}
              </router-link>
            </div>
          </div>
        </div>
      </div>

      <!-- Pagination -->
      <div v-if="totalPages > 1" class="flex justify-center mt-8">
        <nav class="flex items-center space-x-2 rtl:space-x-reverse">
          <button
            @click="currentPage = Math.max(1, currentPage - 1)"
            :disabled="currentPage === 1"
            class="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ $t('common.previous') }}
          </button>
          
          <span class="px-3 py-2 text-sm text-gray-700">
            {{ $t('common.pageOf', 'Page {current} of {total}', { current: currentPage, total: totalPages }) }}
          </span>
          
          <button
            @click="currentPage = Math.min(totalPages, currentPage + 1)"
            :disabled="currentPage === totalPages"
            class="px-3 py-2 text-sm font-medium text-gray-500 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ $t('common.next') }}
          </button>
        </nav>
      </div>
    </div>

    <!-- No Results -->
    <div v-else class="text-center py-12">
      <div class="text-gray-400 mb-4">
        <svg class="w-16 h-16 mx-auto" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9.172 16.172a4 4 0 015.656 0M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" />
        </svg>
      </div>
      <h3 class="text-lg font-medium text-gray-900 mb-2">{{ $t('services.noResults', 'No services found') }}</h3>
      <p class="text-gray-600 mb-4">{{ $t('services.noResultsDescription', 'Try adjusting your search or filter criteria.') }}</p>
      <button @click="clearAllFilters" class="btn btn-primary">
        {{ $t('common.clearAll', 'Clear all filters') }}
      </button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useServicesStore } from '@/stores/services'
import { useLanguageStore } from '@/stores/language'
import ServiceCard from './ServiceCard.vue'

const servicesStore = useServicesStore()
const languageStore = useLanguageStore()

// Reactive state
const loading = ref(false)
const error = ref(null)
const searchQuery = ref('')
const selectedCategory = ref('')
const sortBy = ref('title')
const viewMode = ref('grid')
const currentPage = ref(1)
const itemsPerPage = 12

// Computed properties
const services = computed(() => servicesStore.services)
const categories = computed(() => servicesStore.categories)

const filteredServices = computed(() => {
  let filtered = [...services.value]

  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    filtered = filtered.filter(service => 
      service.title.toLowerCase().includes(query) ||
      service.short_description.toLowerCase().includes(query) ||
      service.description.toLowerCase().includes(query)
    )
  }

  // Apply category filter
  if (selectedCategory.value) {
    filtered = filtered.filter(service => 
      service.category?.id === parseInt(selectedCategory.value)
    )
  }

  // Apply sorting
  filtered.sort((a, b) => {
    switch (sortBy.value) {
      case 'price':
        return a.price_range.localeCompare(b.price_range)
      case 'delivery':
        return a.delivery_time.localeCompare(b.delivery_time)
      case 'featured':
        if (a.is_featured && !b.is_featured) return -1
        if (!a.is_featured && b.is_featured) return 1
        return a.title.localeCompare(b.title)
      case 'title':
      default:
        return a.title.localeCompare(b.title)
    }
  })

  return filtered
})

const totalPages = computed(() => Math.ceil(filteredServices.value.length / itemsPerPage))

const paginatedServices = computed(() => {
  const start = (currentPage.value - 1) * itemsPerPage
  const end = start + itemsPerPage
  return filteredServices.value.slice(start, end)
})

const hasActiveFilters = computed(() => {
  return searchQuery.value || selectedCategory.value
})

// Methods
const getLocalizedRoute = (routeName, params = {}) => {
  return languageStore.getLocalizedRoute(routeName, params)
}

const getCategoryName = (categoryId) => {
  const category = categories.value.find(cat => cat.id === parseInt(categoryId))
  return category ? category.name : ''
}

const clearAllFilters = () => {
  searchQuery.value = ''
  selectedCategory.value = ''
  currentPage.value = 1
}

const fetchServices = async () => {
  loading.value = true
  error.value = null
  
  try {
    await servicesStore.fetchServices()
    await servicesStore.fetchCategories()
  } catch (err) {
    error.value = err.message
    console.error('Error fetching services:', err)
  } finally {
    loading.value = false
  }
}

// Watch for filter changes to reset pagination
watch([searchQuery, selectedCategory, sortBy], () => {
  currentPage.value = 1
})

// Lifecycle
onMounted(() => {
  fetchServices()
})
</script>

<style scoped>
.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors duration-200;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700;
}

/* RTL support for spacing */
.rtl .space-x-2 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}

.rtl .space-x-3 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}

.rtl .space-x-4 > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}

.rtl .space-x-reverse > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}
</style>