<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('close')"></div>

      <!-- Modal panel -->
      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <form @submit.prevent="handleSubmit">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="w-full">
                <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">
                  {{ project?.id ? $t('admin.portfolio.editProject') : $t('admin.portfolio.addNewProject') }}
                </h3>

                <div class="space-y-4">
                  <!-- Project Title -->
                  <div>
                    <label for="title" class="block text-sm font-medium text-gray-700">
                      {{ $t('portfolio.projectTitle') }}
                    </label>
                    <input
                      id="title"
                      v-model="form.title"
                      type="text"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                      :class="{ 'border-red-300': errors.title }"
                    />
                    <div v-if="errors.title" class="mt-1 text-sm text-red-600">
                      {{ errors.title }}
                    </div>
                  </div>

                  <!-- Project Description -->
                  <div>
                    <label for="description" class="block text-sm font-medium text-gray-700">
                      {{ $t('portfolio.projectDescription') }}
                    </label>
                    <textarea
                      id="description"
                      v-model="form.description"
                      rows="3"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                      :class="{ 'border-red-300': errors.description }"
                    ></textarea>
                    <div v-if="errors.description" class="mt-1 text-sm text-red-600">
                      {{ errors.description }}
                    </div>
                  </div>

                  <!-- Category -->
                  <div>
                    <label for="category" class="block text-sm font-medium text-gray-700">
                      {{ $t('portfolio.category') }}
                    </label>
                    <select
                      id="category"
                      v-model="form.category_id"
                      required
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                      :class="{ 'border-red-300': errors.category_id }"
                    >
                      <option value="">{{ $t('portfolio.selectCategory') }}</option>
                      <option v-for="category in categories" :key="category.id" :value="category.id">
                        {{ category.name }}
                      </option>
                    </select>
                    <div v-if="errors.category_id" class="mt-1 text-sm text-red-600">
                      {{ errors.category_id }}
                    </div>
                  </div>

                  <!-- Technologies -->
                  <div>
                    <label for="technologies" class="block text-sm font-medium text-gray-700">
                      {{ $t('portfolio.technologies') }}
                    </label>
                    <input
                      id="technologies"
                      v-model="technologiesInput"
                      type="text"
                      :placeholder="$t('portfolio.technologiesPlaceholder')"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    />
                    <p class="mt-1 text-sm text-gray-500">
                      {{ $t('portfolio.technologiesHelp') }}
                    </p>
                  </div>

                  <!-- Project URL -->
                  <div>
                    <label for="project_url" class="block text-sm font-medium text-gray-700">
                      {{ $t('portfolio.projectUrl') }}
                    </label>
                    <input
                      id="project_url"
                      v-model="form.project_url"
                      type="url"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                      :class="{ 'border-red-300': errors.project_url }"
                    />
                    <div v-if="errors.project_url" class="mt-1 text-sm text-red-600">
                      {{ errors.project_url }}
                    </div>
                  </div>

                  <!-- Image URL -->
                  <div>
                    <label for="image_url" class="block text-sm font-medium text-gray-700">
                      {{ $t('portfolio.imageUrl') }}
                    </label>
                    <input
                      id="image_url"
                      v-model="form.image_url"
                      type="url"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                      :class="{ 'border-red-300': errors.image_url }"
                    />
                    <div v-if="errors.image_url" class="mt-1 text-sm text-red-600">
                      {{ errors.image_url }}
                    </div>
                  </div>

                  <!-- Active Status -->
                  <div class="flex items-center">
                    <input
                      id="is_active"
                      v-model="form.is_active"
                      type="checkbox"
                      class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                    />
                    <label for="is_active" class="ml-2 block text-sm text-gray-900">
                      {{ $t('admin.active') }}
                    </label>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="submit"
              :disabled="loading"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
            >
              <svg v-if="loading" class="animate-spin -ml-1 mr-3 h-5 w-5 text-white" fill="none" viewBox="0 0 24 24">
                <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
                <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
              {{ loading ? $t('common.submitting') : $t('common.save') }}
            </button>
            <button
              type="button"
              @click="$emit('close')"
              class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
            >
              {{ $t('common.cancel') }}
            </button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, watch, computed } from 'vue'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  project: {
    type: Object,
    default: null
  },
  categories: {
    type: Array,
    default: () => []
  }
})

const emit = defineEmits(['close', 'save'])

// State
const loading = ref(false)
const errors = ref({})

// Form data
const form = ref({
  title: '',
  description: '',
  category_id: '',
  project_url: '',
  image_url: '',
  is_active: true,
  technologies: []
})

// Technologies input (comma-separated string)
const technologiesInput = ref('')

// Watch for technologies input changes
watch(technologiesInput, (newValue) => {
  if (newValue) {
    form.value.technologies = newValue.split(',').map(tech => tech.trim()).filter(tech => tech)
  } else {
    form.value.technologies = []
  }
})

// Watch for project changes to populate form
watch(() => props.project, (newProject) => {
  if (newProject) {
    form.value = {
      title: newProject.title || '',
      description: newProject.description || '',
      category_id: newProject.category_id || '',
      project_url: newProject.project_url || '',
      image_url: newProject.image_url || '',
      is_active: newProject.is_active !== undefined ? newProject.is_active : true,
      technologies: newProject.technologies || []
    }
    technologiesInput.value = newProject.technologies ? newProject.technologies.join(', ') : ''
  } else {
    // Reset form for new project
    form.value = {
      title: '',
      description: '',
      category_id: '',
      project_url: '',
      image_url: '',
      is_active: true,
      technologies: []
    }
    technologiesInput.value = ''
  }
  errors.value = {}
}, { immediate: true })

// Methods
const handleSubmit = async () => {
  loading.value = true
  errors.value = {}

  try {
    await emit('save', form.value)
  } catch (error) {
    if (error.response?.data?.errors) {
      errors.value = error.response.data.errors
    } else {
      console.error('Error saving project:', error)
    }
  } finally {
    loading.value = false
  }
}
</script>