import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '../utils/api'

export const useRequestsStore = defineStore('requests', () => {
  const requests = ref([])
  const currentRequest = ref(null)
  const loading = ref(false)
  const submitting = ref(false)
  const error = ref(null)
  const successMessage = ref('')

  // Form data for service requests
  const requestForm = ref({
    service_id: null,
    client_name: '',
    client_email: '',
    client_phone: '',
    project_title: '',
    project_description: '',
    deadline: '',
    budget: '',
    additional_files: []
  })

  // Contact form data
  const contactForm = ref({
    name: '',
    email: '',
    phone: '',
    subject: '',
    message: ''
  })

  // Computed properties
  const pendingRequests = computed(() => 
    requests.value.filter(request => request.status === 'pending')
  )

  const inProgressRequests = computed(() => 
    requests.value.filter(request => request.status === 'in_progress')
  )

  const completedRequests = computed(() => 
    requests.value.filter(request => request.status === 'completed')
  )

  // Actions
  const submitServiceRequest = async (formData) => {
    submitting.value = true
    error.value = null
    successMessage.value = ''
    
    try {
      const response = await api.post('/requests/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data'
        }
      })
      
      successMessage.value = 'Request submitted successfully!'
      resetRequestForm()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to submit request'
      console.error('Error submitting request:', err)
      throw err
    } finally {
      submitting.value = false
    }
  }

  const submitContactForm = async (formData) => {
    submitting.value = true
    error.value = null
    successMessage.value = ''
    
    try {
      const response = await api.post('/contact/', formData)
      successMessage.value = 'Message sent successfully!'
      resetContactForm()
      return response.data
    } catch (err) {
      error.value = err.response?.data?.message || 'Failed to send message'
      console.error('Error submitting contact form:', err)
      throw err
    } finally {
      submitting.value = false
    }
  }

  const fetchRequests = async () => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get('/admin/requests/')
      requests.value = response.data
    } catch (err) {
      error.value = 'Failed to fetch requests'
      console.error('Error fetching requests:', err)
    } finally {
      loading.value = false
    }
  }

  const getRequestDetails = async (id) => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.get(`/admin/requests/${id}/`)
      currentRequest.value = response.data
      return response.data
    } catch (err) {
      error.value = 'Failed to fetch request details'
      console.error('Error fetching request details:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const updateRequestStatus = async (id, status, notes = '') => {
    loading.value = true
    error.value = null
    
    try {
      const response = await api.patch(`/admin/requests/${id}/`, {
        status,
        notes
      })
      
      // Update the request in the local state
      const index = requests.value.findIndex(req => req.id === id)
      if (index !== -1) {
        requests.value[index] = response.data
      }
      
      if (currentRequest.value && currentRequest.value.id === id) {
        currentRequest.value = response.data
      }
      
      successMessage.value = 'Request status updated successfully!'
      return response.data
    } catch (err) {
      error.value = 'Failed to update request status'
      console.error('Error updating request status:', err)
      throw err
    } finally {
      loading.value = false
    }
  }

  const setRequestFormData = (data) => {
    requestForm.value = { ...requestForm.value, ...data }
  }

  const setContactFormData = (data) => {
    contactForm.value = { ...contactForm.value, ...data }
  }

  const resetRequestForm = () => {
    requestForm.value = {
      service_id: null,
      client_name: '',
      client_email: '',
      client_phone: '',
      project_title: '',
      project_description: '',
      deadline: '',
      budget: '',
      additional_files: []
    }
  }

  const resetContactForm = () => {
    contactForm.value = {
      name: '',
      email: '',
      phone: '',
      subject: '',
      message: ''
    }
  }

  const clearError = () => {
    error.value = null
  }

  const clearSuccessMessage = () => {
    successMessage.value = ''
  }

  return {
    // State
    requests,
    currentRequest,
    loading,
    submitting,
    error,
    successMessage,
    requestForm,
    contactForm,
    
    // Computed
    pendingRequests,
    inProgressRequests,
    completedRequests,
    
    // Actions
    submitServiceRequest,
    submitContactForm,
    fetchRequests,
    getRequestDetails,
    updateRequestStatus,
    setRequestFormData,
    setContactFormData,
    resetRequestForm,
    resetContactForm,
    clearError,
    clearSuccessMessage
  }
})