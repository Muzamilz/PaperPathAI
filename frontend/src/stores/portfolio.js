import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../utils/api'

export const usePortfolioStore = defineStore('portfolio', () => {
  const portfolioItems = ref([])
  const currentItem = ref(null)
  const loading = ref(false)
  const error = ref(null)
  const selectedCategory = ref(null)

  // Computed properties
  const featuredItems = computed(() => 
    portfolioItems.value.filter(item => item.is_featured && item.is_active)
  )

  const filteredItems = computed(() => {
    let filtered = portfolioItems.value.filter(item => item.is_active)

    if (selectedCategory.value) {
      filtered = filtered.filter(item => 
        item.service_category_id === selectedCategory.value
      )
    }

    return filtered.sort((a, b) => {
      // Sort by order first, then by completion date (newest first)
      if (a.order !== b.order) {
        return a.order - b.order
      }
      return new Date(b.completion_date) - new Date(a.completion_date)
    })
  })

  const categories = computed(() => {
    const categoryMap = new Map()
    portfolioItems.value.forEach(item => {
      if (item.service_category && !categoryMap.has(item.service_category.id)) {
        categoryMap.set(item.service_category.id, item.service_category)
      }
    })
    return Array.from(categoryMap.values())
  })

  // Actions
  const fetchPortfolioItems = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get('/portfolio/')
      portfolioItems.value = Array.isArray(response.data) ? response.data : response.data.results || []
    } catch (err) {
      error.value = 'Failed to fetch portfolio items'
      console.error('Error fetching portfolio items:', err)
      portfolioItems.value = [] // Ensure portfolioItems is always an array
    } finally {
      loading.value = false
    }
  }

  const getPortfolioItemDetails = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get(`/portfolio/${id}/`)
      currentItem.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Failed to fetch portfolio item details'
      console.error('Error fetching portfolio item details:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const setSelectedCategory = (categoryId) => {
    selectedCategory.value = categoryId
  }

  const clearFilters = () => {
    selectedCategory.value = null
  }

  const clearError = () => {
    error.value = null
  }

  return {
    // State
    portfolioItems,
    items: portfolioItems, // Add alias for compatibility
    currentItem,
    loading,
    error,
    selectedCategory,
    
    // Computed
    featuredItems,
    filteredItems,
    categories,
    
    // Actions
    fetchPortfolioItems,
    getPortfolioItemDetails,
    setSelectedCategory,
    clearFilters,
    clearError
  }
})