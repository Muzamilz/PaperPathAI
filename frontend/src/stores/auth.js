import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/utils/api'

export const useAuthStore = defineStore('auth', () => {
  // State
  const user = ref(null)
  const token = ref(localStorage.getItem('auth_token'))
  const loading = ref(false)
  const error = ref(null)

  // Getters
  const isAuthenticated = computed(() => !!token.value && !!user.value)
  const isAdmin = computed(() => user.value?.is_staff || user.value?.is_superuser)

  // Actions
  const login = async (credentials) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.post('/auth/login/', credentials)
      const { token: authToken, user: userData } = response.data
      
      token.value = authToken
      user.value = userData
      
      // Store token in localStorage
      localStorage.setItem('auth_token', authToken)
      
      // Set default authorization header
      api.defaults.headers.common['Authorization'] = `Token ${authToken}`
      
      return { success: true }
    } catch (err) {
      error.value = err.response?.data?.error?.message || 'Login failed'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  const logout = async () => {
    loading.value = true
    
    try {
      if (token.value) {
        await api.post('/auth/logout/')
      }
    } catch (err) {
      console.error('Logout error:', err)
    } finally {
      // Clear local state regardless of API call success
      token.value = null
      user.value = null
      localStorage.removeItem('auth_token')
      delete api.defaults.headers.common['Authorization']
      loading.value = false
    }
  }

  const checkAuth = async () => {
    if (!token.value) return false
    
    loading.value = true
    
    try {
      // Set authorization header
      api.defaults.headers.common['Authorization'] = `Token ${token.value}`
      
      // Verify token and get user data
      const response = await api.get('/auth/me/')
      user.value = response.data
      
      return true
    } catch (err) {
      // Token is invalid, clear it
      token.value = null
      user.value = null
      localStorage.removeItem('auth_token')
      delete api.defaults.headers.common['Authorization']
      
      return false
    } finally {
      loading.value = false
    }
  }

  const refreshUser = async () => {
    if (!token.value) return
    
    try {
      const response = await api.get('/auth/me/')
      user.value = response.data
    } catch (err) {
      console.error('Failed to refresh user data:', err)
    }
  }

  // Initialize auth state on store creation
  if (token.value) {
    checkAuth()
  }

  return {
    // State
    user,
    token,
    loading,
    error,
    
    // Getters
    isAuthenticated,
    isAdmin,
    
    // Actions
    login,
    logout,
    checkAuth,
    refreshUser
  }
})