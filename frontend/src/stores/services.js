import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../utils/api'

export const useServicesStore = defineStore('services', () => {
  const categories = ref([])
  const services = ref([])
  const currentService = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const searchQuery = ref('')
  const selectedCategory = ref(null)

  // Computed properties
  const filteredServices = computed(() => {
    let filtered = services.value

    // Filter by category
    if (selectedCategory.value) {
      filtered = filtered.filter(service => 
        service.category_id === selectedCategory.value
      )
    }

    // Filter by search query
    if (searchQuery.value) {
      const query = searchQuery.value.toLowerCase()
      filtered = filtered.filter(service =>
        service.title.toLowerCase().includes(query) ||
        service.description.toLowerCase().includes(query)
      )
    }

    return filtered
  })

  const activeCategories = computed(() => 
    categories.value.filter(category => category.is_active)
  )

  // Actions
  const fetchCategories = async () => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get('/services/categories/')
      categories.value = Array.isArray(response.data) ? response.data : response.data.results || []
    } catch (err) {
      error.value = 'Failed to fetch categories'
      console.error('Error fetching categories:', err)
      categories.value = [] // Ensure categories is always an array
    } finally {
      loading.value = false
    }
  }

  const fetchServices = async (categoryId = null) => {
    loading.value = true
    error.value = null
    try {
      const url = categoryId 
        ? `/services/categories/${categoryId}/`
        : '/services/'
      const response = await api.get(url)
      
      if (categoryId) {
        // If fetching by category, response contains category with services
        services.value = response.data.services || []
      } else {
        // If fetching all services
        services.value = Array.isArray(response.data) ? response.data : response.data.results || []
      }
    } catch (err) {
      error.value = 'Failed to fetch services'
      console.error('Error fetching services:', err)
      services.value = [] // Ensure services is always an array
    } finally {
      loading.value = false
    }
  }

  const getServiceDetails = async (id) => {
    loading.value = true
    error.value = null
    try {
      const response = await api.get(`/services/${id}/`)
      currentService.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Failed to fetch service details'
      console.error('Error fetching service details:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const setSearchQuery = (query) => {
    searchQuery.value = query
  }

  const setSelectedCategory = (categoryId) => {
    selectedCategory.value = categoryId
  }

  const clearFilters = () => {
    searchQuery.value = ''
    selectedCategory.value = null
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    categories,
    services,
    currentService,
    loading,
    error,
    searchQuery,
    selectedCategory,
    
    // Computed
    filteredServices,
    activeCategories,
    
    // Actions
    fetchCategories,
    fetchServices,
    getServiceDetails,
    setSearchQuery,
    setSelectedCategory,
    clearFilters,
    clearError
  }
})