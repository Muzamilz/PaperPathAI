<template>
  <div class="px-4 sm:px-6 lg:px-8">
    <!-- Page Header -->
    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <h1 class="text-2xl font-semibold text-gray-900">{{ $t('admin.services') }}</h1>
        <p class="mt-2 text-sm text-gray-700">
          {{ $t('admin.services.manageServices') }}
        </p>
      </div>
      <div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
        <button
          @click="showCreateModal = true"
          type="button"
          class="inline-flex items-center justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 sm:w-auto"
        >
          <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
          </svg>
          {{ $t('admin.services.addNewService') }}
        </button>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="mt-6 bg-white shadow rounded-lg p-4">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-3">
        <!-- Search -->
        <div>
          <label for="search" class="block text-sm font-medium text-gray-700">{{ $t('admin.search') }}</label>
          <input
            id="search"
            v-model="filters.search"
            type="text"
            :placeholder="$t('admin.search')"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          />
        </div>

        <!-- Category Filter -->
        <div>
          <label for="category" class="block text-sm font-medium text-gray-700">{{ $t('services.categories') }}</label>
          <select
            id="category"
            v-model="filters.category"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          >
            <option value="">{{ $t('portfolio.allCategories') }}</option>
            <option v-for="category in categories" :key="category.id" :value="category.id">
              {{ category.name }}
            </option>
          </select>
        </div>

        <!-- Status Filter -->
        <div>
          <label for="status" class="block text-sm font-medium text-gray-700">Status</label>
          <select
            id="status"
            v-model="filters.status"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          >
            <option value="">All Status</option>
            <option value="true">Active</option>
            <option value="false">Inactive</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Services Table -->
    <div class="mt-6 bg-white shadow rounded-lg overflow-hidden">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-2 text-sm text-gray-500">{{ $t('common.loading') }}</p>
      </div>

      <div v-else-if="filteredServices.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">No services found</h3>
        <p class="mt-1 text-sm text-gray-500">Get started by creating a new service.</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Service
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Category
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Price Range
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Status
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                Requests
              </th>
              <th class="relative px-6 py-3">
                <span class="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="service in filteredServices" :key="service.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ service.title }}</div>
                    <div class="text-sm text-gray-500">{{ truncateText(service.short_description, 60) }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                  {{ service.category?.name || 'No Category' }}
                </span>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                {{ service.price_range || 'Contact for pricing' }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <button
                  @click="toggleServiceStatus(service)"
                  :class="service.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                  class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium cursor-pointer hover:opacity-80"
                >
                  {{ service.is_active ? 'Active' : 'Inactive' }}
                </button>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-500">
                {{ service.request_count || 0 }}
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center space-x-2">
                  <button
                    @click="editService(service)"
                    class="text-blue-600 hover:text-blue-900"
                  >
                    {{ $t('common.edit') }}
                  </button>
                  <button
                    @click="deleteService(service)"
                    class="text-red-600 hover:text-red-900"
                  >
                    {{ $t('common.delete') }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Create/Edit Service Modal -->
    <ServiceModal
      v-if="showCreateModal || showEditModal"
      :show="showCreateModal || showEditModal"
      :service="editingService"
      :categories="categories"
      @close="closeModal"
      @save="handleSaveService"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      v-if="showDeleteModal"
      :show="showDeleteModal"
      title="Delete Service"
      :message="`Are you sure you want to delete '${deletingService?.title}'? This action cannot be undone.`"
      confirm-text="Delete"
      confirm-class="bg-red-600 hover:bg-red-700"
      @close="showDeleteModal = false"
      @confirm="confirmDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import api from '@/utils/api'
import ServiceModal from '@/components/admin/ServiceModal.vue'
import ConfirmModal from '@/components/admin/ConfirmModal.vue'

// State
const loading = ref(true)
const services = ref([])
const categories = ref([])
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const editingService = ref(null)
const deletingService = ref(null)

// Filters
const filters = ref({
  search: '',
  category: '',
  status: ''
})

// Computed
const filteredServices = computed(() => {
  let filtered = services.value

  // Search filter
  if (filters.value.search) {
    const searchTerm = filters.value.search.toLowerCase()
    filtered = filtered.filter(service =>
      service.title.toLowerCase().includes(searchTerm) ||
      service.short_description.toLowerCase().includes(searchTerm) ||
      service.category?.name.toLowerCase().includes(searchTerm)
    )
  }

  // Category filter
  if (filters.value.category) {
    filtered = filtered.filter(service => 
      service.category?.id === parseInt(filters.value.category)
    )
  }

  // Status filter
  if (filters.value.status !== '') {
    const isActive = filters.value.status === 'true'
    filtered = filtered.filter(service => service.is_active === isActive)
  }

  return filtered
})

// Methods
const fetchServices = async () => {
  try {
    loading.value = true
    const response = await api.get('/services/admin/services/')
    services.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to fetch services:', error)
    services.value = []
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const response = await api.get('/services/admin/categories/')
    categories.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to fetch categories:', error)
    categories.value = []
  }
}

const editService = (service) => {
  editingService.value = { ...service }
  showEditModal.value = true
}

const deleteService = (service) => {
  deletingService.value = service
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    await api.delete(`/services/admin/services/${deletingService.value.id}/`)
    services.value = services.value.filter(s => s.id !== deletingService.value.id)
    showDeleteModal.value = false
    deletingService.value = null
  } catch (error) {
    console.error('Failed to delete service:', error)
  }
}

const toggleServiceStatus = async (service) => {
  try {
    const updatedService = { ...service, is_active: !service.is_active }
    await api.patch(`/services/admin/services/${service.id}/`, { is_active: updatedService.is_active })
    
    // Update local state
    const index = services.value.findIndex(s => s.id === service.id)
    if (index !== -1) {
      services.value[index] = updatedService
    }
  } catch (error) {
    console.error('Failed to update service status:', error)
  }
}

const handleSaveService = async (serviceData) => {
  try {
    if (editingService.value?.id) {
      // Update existing service
      const response = await api.patch(`/services/admin/services/${editingService.value.id}/`, serviceData)
      const index = services.value.findIndex(s => s.id === editingService.value.id)
      if (index !== -1) {
        services.value[index] = response.data
      }
    } else {
      // Create new service
      const response = await api.post('/services/admin/services/', serviceData)
      services.value.unshift(response.data)
    }
    closeModal()
  } catch (error) {
    console.error('Failed to save service:', error)
    throw error
  }
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingService.value = null
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

// Lifecycle
onMounted(() => {
  fetchServices()
  fetchCategories()
})
</script>