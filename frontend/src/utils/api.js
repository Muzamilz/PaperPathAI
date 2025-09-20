import axios from 'axios'
import { useLanguageStore } from '../stores/language'

// Create axios instance with default configuration
const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  }
})

// Set authorization header if token exists in localStorage
const token = localStorage.getItem('auth_token')
if (token) {
  api.defaults.headers.common['Authorization'] = `Token ${token}`
}

// Request interceptor to add language header and ensure auth token
api.interceptors.request.use(
  (config) => {
    const languageStore = useLanguageStore()
    config.headers['Accept-Language'] = languageStore.currentLanguage
    
    // Ensure auth token is always included if available
    const token = localStorage.getItem('auth_token')
    if (token && !config.headers['Authorization']) {
      config.headers['Authorization'] = `Token ${token}`
    }
    
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response
  },
  (error) => {
    // Handle common errors
    if (error.response) {
      // Server responded with error status
      const { status, data } = error.response
      
      switch (status) {
        case 401:
          // Unauthorized - clear token and redirect to login
          console.error('Unauthorized access')
          localStorage.removeItem('auth_token')
          delete api.defaults.headers.common['Authorization']
          // Only redirect if not already on login page
          if (window.location.pathname !== '/en/admin/login' && window.location.pathname !== '/ar/admin/login') {
            window.location.href = '/en/admin/login'
          }
          break
        case 403:
          // Forbidden
          console.error('Access forbidden')
          break
        case 404:
          // Not found
          console.error('Resource not found')
          break
        case 422:
          // Validation error
          console.error('Validation error:', data)
          break
        case 500:
          // Server error
          console.error('Server error')
          break
        default:
          console.error('API error:', error.response)
      }
    } else if (error.request) {
      // Network error
      console.error('Network error:', error.request)
    } else {
      // Other error
      console.error('Error:', error.message)
    }
    
    return Promise.reject(error)
  }
)

export default api