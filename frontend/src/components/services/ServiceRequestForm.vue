<template>
  <div class="bg-white rounded-2xl p-8 shadow-sm">
    <form @submit.prevent="handleSubmit" class="space-y-6">
      <!-- Project Title -->
      <div>
        <label for="projectTitle" class="block text-sm font-medium text-gray-700 mb-2">Project Title</label>
        <input
          id="projectTitle"
          v-model="form.projectTitle"
          type="text"
          placeholder="Enter project title"
          :class="[
            'w-full px-4 py-3 bg-gray-100 border-0 rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white transition-colors duration-200',
            errors.projectTitle ? 'ring-2 ring-red-300' : ''
          ]"
          required
        />
        <p v-if="errors.projectTitle" class="mt-1 text-sm text-red-600">{{ errors.projectTitle }}</p>
      </div>

      <!-- Service Type -->
      <div>
        <label for="serviceType" class="block text-sm font-medium text-gray-700 mb-2">Service Type</label>
        <div class="relative">
          <select
            id="serviceType"
            v-model="form.serviceId"
            :class="[
              'w-full px-4 py-3 bg-gray-100 border-0 rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white transition-colors duration-200 appearance-none',
              errors.serviceId ? 'ring-2 ring-red-300' : ''
            ]"
            required
          >
            <option value="">Select a service...</option>
            <option 
              v-for="service in services" 
              :key="service.id" 
              :value="service.id"
            >
              {{ service.title }}
            </option>
          </select>
          <div class="absolute inset-y-0 right-0 flex items-center pr-4 pointer-events-none">
            <svg class="w-5 h-5 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 9l-7 7-7-7" />
            </svg>
          </div>
        </div>
        <p v-if="errors.serviceId" class="mt-1 text-sm text-red-600">{{ errors.serviceId }}</p>
      </div>

      <!-- Project Description -->
      <div>
        <label for="projectDescription" class="block text-sm font-medium text-gray-700 mb-2">Project Description</label>
        <textarea
          id="projectDescription"
          v-model="form.projectDescription"
          rows="5"
          placeholder="Describe your project in detail"
          :class="[
            'w-full px-4 py-3 bg-gray-100 border-0 rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white transition-colors duration-200 resize-none',
            errors.projectDescription ? 'ring-2 ring-red-300' : ''
          ]"
          required
        ></textarea>
        <p v-if="errors.projectDescription" class="mt-1 text-sm text-red-600">{{ errors.projectDescription }}</p>
      </div>

      <!-- Desired Deadline -->
      <div>
        <label for="deadline" class="block text-sm font-medium text-gray-700 mb-2">Desired Deadline</label>
        <input
          id="deadline"
          v-model="form.deadline"
          type="date"
          :class="[
            'w-full px-4 py-3 bg-gray-100 border-0 rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white transition-colors duration-200',
            errors.deadline ? 'ring-2 ring-red-300' : ''
          ]"
        />
        <p v-if="errors.deadline" class="mt-1 text-sm text-red-600">{{ errors.deadline }}</p>
      </div>

      <!-- Contact Email -->
      <div>
        <label for="email" class="block text-sm font-medium text-gray-700 mb-2">Contact Email</label>
        <input
          id="email"
          v-model="form.email"
          type="email"
          placeholder="Enter your email"
          :class="[
            'w-full px-4 py-3 bg-gray-100 border-0 rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white transition-colors duration-200',
            errors.email ? 'ring-2 ring-red-300' : ''
          ]"
          required
        />
        <p v-if="errors.email" class="mt-1 text-sm text-red-600">{{ errors.email }}</p>
      </div>

      <!-- Contact Phone -->
      <div>
        <label for="phone" class="block text-sm font-medium text-gray-700 mb-2">Contact Phone</label>
        <input
          id="phone"
          v-model="form.phone"
          type="tel"
          placeholder="Enter your phone number"
          :class="[
            'w-full px-4 py-3 bg-gray-100 border-0 rounded-xl focus:ring-2 focus:ring-blue-500 focus:bg-white transition-colors duration-200',
            errors.phone ? 'ring-2 ring-red-300' : ''
          ]"
        />
        <p v-if="errors.phone" class="mt-1 text-sm text-red-600">{{ errors.phone }}</p>
      </div>

      <!-- Submit Button -->
      <div class="pt-4">
        <button
          type="submit"
          :disabled="isSubmitting"
          :class="[
            'w-full flex justify-center py-3 px-6 border border-transparent rounded-xl text-base font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 transition-colors duration-200',
            isSubmitting 
              ? 'bg-gray-400 cursor-not-allowed' 
              : 'bg-blue-600 hover:bg-blue-700'
          ]"
        >
          <svg v-if="isSubmitting" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
          </svg>
          {{ isSubmitting ? 'Submitting...' : 'Submit Request' }}
        </button>
      </div>
    </form>

    <!-- Success Message -->
    <div v-if="showSuccess" class="mt-6 p-4 bg-green-100 border border-green-400 text-green-700 rounded-xl">
      <div class="flex">
        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" />
        </svg>
        Request submitted successfully! We'll get back to you soon.
      </div>
    </div>

    <!-- Error Message -->
    <div v-if="showError" class="mt-6 p-4 bg-red-100 border border-red-400 text-red-700 rounded-xl">
      <div class="flex">
        <svg class="w-5 h-5 mr-2" fill="currentColor" viewBox="0 0 20 20">
          <path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z" clip-rule="evenodd" />
        </svg>
        Failed to submit request. Please try again.
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, computed, onMounted } from 'vue'
import { useServicesStore } from '@/stores/services'
import api from '@/utils/api'

const servicesStore = useServicesStore()

// Props
const props = defineProps({
  serviceId: {
    type: [String, Number],
    default: null
  }
})

// Form data
const form = reactive({
  projectTitle: '',
  serviceId: props.serviceId || '',
  projectDescription: '',
  deadline: '',
  email: '',
  phone: ''
})

// Form state
const isSubmitting = ref(false)
const showSuccess = ref(false)
const showError = ref(false)
const errors = reactive({})

// Computed properties
const services = computed(() => servicesStore.services)

// Validation
const validateForm = () => {
  const newErrors = {}

  if (!form.projectTitle.trim()) {
    newErrors.projectTitle = 'Project title is required'
  }

  if (!form.serviceId) {
    newErrors.serviceId = 'Service selection is required'
  }

  if (!form.projectDescription.trim()) {
    newErrors.projectDescription = 'Project description is required'
  } else if (form.projectDescription.trim().length < 20) {
    newErrors.projectDescription = 'Project description must be at least 20 characters long'
  }

  if (!form.email.trim()) {
    newErrors.email = 'Email is required'
  } else if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(form.email)) {
    newErrors.email = 'Please enter a valid email address'
  }

  if (form.phone && !/^[\+]?[1-9][\d]{0,15}$/.test(form.phone.replace(/\s/g, ''))) {
    newErrors.phone = 'Please enter a valid phone number'
  }

  Object.keys(errors).forEach(key => delete errors[key])
  Object.assign(errors, newErrors)

  return Object.keys(newErrors).length === 0
}

// Submit form
const handleSubmit = async () => {
  if (!validateForm()) {
    return
  }

  isSubmitting.value = true
  showSuccess.value = false
  showError.value = false

  try {
    await api.post('/requests/', {
      project_title: form.projectTitle.trim(),
      service: form.serviceId,
      project_description: form.projectDescription.trim(),
      deadline: form.deadline || null,
      client_email: form.email.trim(),
      client_phone: form.phone.trim()
    })

    showSuccess.value = true
    
    // Reset form
    Object.keys(form).forEach(key => {
      if (key === 'serviceId' && props.serviceId) {
        form[key] = props.serviceId
      } else {
        form[key] = ''
      }
    })

    // Hide success message after 5 seconds
    setTimeout(() => {
      showSuccess.value = false
    }, 5000)

  } catch (error) {
    console.error('Error submitting service request:', error)
    showError.value = true
    
    // Handle validation errors from server
    if (error.response?.data?.errors) {
      Object.assign(errors, error.response.data.errors)
    }

    // Hide error message after 5 seconds
    setTimeout(() => {
      showError.value = false
    }, 5000)
  } finally {
    isSubmitting.value = false
  }
}

// Lifecycle
onMounted(() => {
  servicesStore.fetchServices()
})
</script>