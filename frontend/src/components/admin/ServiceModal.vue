<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('close')"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
        <form @submit.prevent="handleSubmit">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                  {{ service?.id ? 'Edit Service' : 'Create New Service' }}
                </h3>

                <div class="grid grid-cols-1 gap-4 sm:grid-cols-2">
                  <!-- Title -->
                  <div class="sm:col-span-2">
                    <label for="title" class="block text-sm font-medium text-gray-700">Title *</label>
                    <input
                      id="title"
                      v-model="form.title"
                      type="text"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                      :class="{ 'border-red-300': errors.title }"
                    />
                    <p v-if="errors.title" class="mt-1 text-sm text-red-600">{{ errors.title }}</p>
                  </div>

                  <!-- Category -->
                  <div>
                    <label for="category" class="block text-sm font-medium text-gray-700">Category *</label>
                    <select
                      id="category"
                      v-model="form.category"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                      :class="{ 'border-red-300': errors.category }"
                    >
                      <option value="">Select a category</option>
                      <option v-for="category in categories" :key="category.id" :value="category.id">
                        {{ category.name }}
                      </option>
                    </select>
                    <p v-if="errors.category" class="mt-1 text-sm text-red-600">{{ errors.category }}</p>
                  </div>

                  <!-- Price Range -->
                  <div>
                    <label for="price_range" class="block text-sm font-medium text-gray-700">Price Range</label>
                    <input
                      id="price_range"
                      v-model="form.price_range"
                      type="text"
                      placeholder="e.g., $100 - $500"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    />
                  </div>

                  <!-- Delivery Time -->
                  <div>
                    <label for="delivery_time" class="block text-sm font-medium text-gray-700">Delivery Time</label>
                    <input
                      id="delivery_time"
                      v-model="form.delivery_time"
                      type="text"
                      placeholder="e.g., 3-5 business days"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    />
                  </div>

                  <!-- Order -->
                  <div>
                    <label for="order" class="block text-sm font-medium text-gray-700">Display Order</label>
                    <input
                      id="order"
                      v-model.number="form.order"
                      type="number"
                      min="0"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    />
                  </div>

                  <!-- Short Description -->
                  <div class="sm:col-span-2">
                    <label for="short_description" class="block text-sm font-medium text-gray-700">Short Description</label>
                    <textarea
                      id="short_description"
                      v-model="form.short_description"
                      rows="2"
                      maxlength="300"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                      placeholder="Brief description for service cards..."
                    ></textarea>
                    <p class="mt-1 text-sm text-gray-500">{{ form.short_description?.length || 0 }}/300 characters</p>
                  </div>

                  <!-- Description -->
                  <div class="sm:col-span-2">
                    <label for="description" class="block text-sm font-medium text-gray-700">Full Description *</label>
                    <textarea
                      id="description"
                      v-model="form.description"
                      rows="4"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                      :class="{ 'border-red-300': errors.description }"
                      placeholder="Detailed description of the service..."
                    ></textarea>
                    <p v-if="errors.description" class="mt-1 text-sm text-red-600">{{ errors.description }}</p>
                  </div>

                  <!-- Features -->
                  <div class="sm:col-span-2">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Features</label>
                    <div class="space-y-2">
                      <div v-for="(feature, index) in form.features" :key="index" class="flex items-center space-x-2">
                        <input
                          v-model="form.features[index]"
                          type="text"
                          placeholder="Enter a feature..."
                          class="flex-1 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                        />
                        <button
                          type="button"
                          @click="removeFeature(index)"
                          class="text-red-600 hover:text-red-800"
                        >
                          <svg class="h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                          </svg>
                        </button>
                      </div>
                      <button
                        type="button"
                        @click="addFeature"
                        class="inline-flex items-center px-3 py-1 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500"
                      >
                        <svg class="-ml-1 mr-1 h-4 w-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
                        </svg>
                        Add Feature
                      </button>
                    </div>
                  </div>

                  <!-- Status -->
                  <div class="sm:col-span-2">
                    <div class="flex items-center">
                      <input
                        id="is_active"
                        v-model="form.is_active"
                        type="checkbox"
                        class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                      />
                      <label for="is_active" class="ml-2 block text-sm text-gray-900">
                        Active (visible to users)
                      </label>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="submit"
              :disabled="submitting"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              <svg v-if="submitting" class="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ submitting ? 'Saving...' : (service?.id ? 'Update Service' : 'Create Service') }}
            </button>
            <button
              type="button"
              @click="$emit('close')"
              :disabled="submitting"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
            >
              Cancel
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch } from 'vue'

const props = defineProps({
  show: Boolean,
  service: Object,
  categories: Array
})

const emit = defineEmits(['close', 'save'])

// State
const submitting = ref(false)
const errors = ref({})

// Form data
const form = reactive({
  title: '',
  category: '',
  short_description: '',
  description: '',
  price_range: '',
  delivery_time: '',
  features: [''],
  is_active: true,
  order: 0
})

// Methods
const resetForm = () => {
  form.title = ''
  form.category = ''
  form.short_description = ''
  form.description = ''
  form.price_range = ''
  form.delivery_time = ''
  form.features = ['']
  form.is_active = true
  form.order = 0
  errors.value = {}
}

const populateForm = (service) => {
  if (service) {
    form.title = service.title || ''
    form.category = service.category?.id || ''
    form.short_description = service.short_description || ''
    form.description = service.description || ''
    form.price_range = service.price_range || ''
    form.delivery_time = service.delivery_time || ''
    form.features = service.features?.length ? [...service.features] : ['']
    form.is_active = service.is_active !== false
    form.order = service.order || 0
  } else {
    resetForm()
  }
}

const addFeature = () => {
  form.features.push('')
}

const removeFeature = (index) => {
  if (form.features.length > 1) {
    form.features.splice(index, 1)
  }
}

const validateForm = () => {
  errors.value = {}

  if (!form.title.trim()) {
    errors.value.title = 'Title is required'
  }

  if (!form.category) {
    errors.value.category = 'Category is required'
  }

  if (!form.description.trim()) {
    errors.value.description = 'Description is required'
  }

  return Object.keys(errors.value).length === 0
}

const handleSubmit = async () => {
  if (!validateForm()) return

  try {
    submitting.value = true

    // Clean up features (remove empty ones)
    const cleanFeatures = form.features.filter(f => f.trim())

    const serviceData = {
      title: form.title.trim(),
      category: form.category,
      short_description: form.short_description.trim(),
      description: form.description.trim(),
      price_range: form.price_range.trim(),
      delivery_time: form.delivery_time.trim(),
      features: cleanFeatures,
      is_active: form.is_active,
      order: form.order
    }

    await emit('save', serviceData)
  } catch (error) {
    console.error('Form submission error:', error)
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    }
  } finally {
    submitting.value = false
  }
}

// Watch for service changes
watch(() => props.service, (newService) => {
  populateForm(newService)
}, { immediate: true })

// Watch for show changes to reset form
watch(() => props.show, (show) => {
  if (show && !props.service) {
    resetForm()
  }
})
</script>