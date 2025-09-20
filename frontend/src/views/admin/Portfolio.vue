<template>
  <div class="px-4 sm:px-6 lg:px-8">
    <!-- Page Header -->
    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <h1 class="text-2xl font-semibold text-gray-900">{{ $t('admin.portfolio') }}</h1>
        <p class="mt-2 text-sm text-gray-700">
          {{ $t('admin.portfolio.managePortfolio') }}
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
          {{ $t('admin.portfolio.addNewProject') }}
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
          <label for="status" class="block text-sm font-medium text-gray-700">{{ $t('admin.status') }}</label>
          <select
            id="status"
            v-model="filters.status"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          >
            <option value="">{{ $t('common.all') }}</option>
            <option value="true">{{ $t('admin.active') }}</option>
            <option value="false">{{ $t('admin.inactive') }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Portfolio Grid -->
    <div class="mt-6 bg-white shadow rounded-lg overflow-hidden">
      <div v-if="loading" class="text-center py-12">
        <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
        <p class="mt-2 text-sm text-gray-500">{{ $t('common.loading') }}</p>
      </div>

      <div v-else-if="filteredPortfolio.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">{{ $t('admin.portfolio.noProjectsFound') }}</h3>
        <p class="mt-1 text-sm text-gray-500">{{ $t('admin.portfolio.createFirstProject') }}</p>
      </div>

      <div v-else class="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-3 p-6">
        <div
          v-for="project in filteredPortfolio"
          :key="project.id"
          class="bg-white border border-gray-200 rounded-lg shadow-sm hover:shadow-md transition-shadow duration-200"
        >
          <!-- Project Image -->
          <div class="aspect-w-16 aspect-h-9 bg-gray-200 rounded-t-lg overflow-hidden">
            <img
              v-if="project.image"
              :src="project.image"
              :alt="project.title"
              class="w-full h-48 object-cover"
            />
            <div v-else class="w-full h-48 bg-gradient-to-br from-blue-400 to-blue-600 flex items-center justify-center">
              <svg class="w-12 h-12 text-white opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
              </svg>
            </div>
          </div>

          <!-- Project Info -->
          <div class="p-4">
            <div class="flex items-start justify-between">
              <div class="flex-1">
                <h3 class="text-lg font-medium text-gray-900 mb-1">{{ project.title }}</h3>
                <p class="text-sm text-gray-600 mb-2">{{ truncateText(project.description, 100) }}</p>
                
                <!-- Category and Status -->
                <div class="flex items-center space-x-2 mb-3">
                  <span class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800">
                    {{ project.category?.name || $t('portfolio.category') }}
                  </span>
                  <button
                    @click="toggleProjectStatus(project)"
                    :class="project.is_active ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'"
                    class="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium cursor-pointer hover:opacity-80"
                  >
                    {{ project.is_active ? $t('admin.active') : $t('admin.inactive') }}
                  </button>
                </div>

                <!-- Technologies -->
                <div v-if="project.technologies && project.technologies.length" class="mb-3">
                  <div class="flex flex-wrap gap-1">
                    <span
                      v-for="tech in project.technologies.slice(0, 3)"
                      :key="tech"
                      class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800"
                    >
                      {{ tech }}
                    </span>
                    <span
                      v-if="project.technologies.length > 3"
                      class="inline-flex items-center px-2 py-1 rounded text-xs font-medium bg-gray-100 text-gray-800"
                    >
                      +{{ project.technologies.length - 3 }} {{ $t('common.more') }}
                    </span>
                  </div>
                </div>
              </div>
            </div>

            <!-- Actions -->
            <div class="flex items-center justify-between pt-3 border-t border-gray-200">
              <div class="flex items-center space-x-2">
                <button
                  @click="editProject(project)"
                  class="text-blue-600 hover:text-blue-900 text-sm font-medium"
                >
                  {{ $t('common.edit') }}
                </button>
                <button
                  @click="deleteProject(project)"
                  class="text-red-600 hover:text-red-900 text-sm font-medium"
                >
                  {{ $t('common.delete') }}
                </button>
              </div>
              <div class="text-xs text-gray-500">
                {{ formatDate(project.created_at) }}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- Create/Edit Project Modal -->
    <PortfolioModal
      v-if="showCreateModal || showEditModal"
      :show="showCreateModal || showEditModal"
      :project="editingProject"
      :categories="categories"
      @close="closeModal"
      @save="handleSaveProject"
    />

    <!-- Delete Confirmation Modal -->
    <ConfirmModal
      v-if="showDeleteModal"
      :show="showDeleteModal"
      :title="$t('admin.portfolio.deleteProject')"
      :message="$t('admin.portfolio.confirmDelete', { title: deletingProject?.title })"
      :confirm-text="$t('common.delete')"
      confirm-class="bg-red-600 hover:bg-red-700"
      @close="showDeleteModal = false"
      @confirm="confirmDelete"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '@/utils/api'
import PortfolioModal from '@/components/admin/PortfolioModal.vue'
import ConfirmModal from '@/components/admin/ConfirmModal.vue'

// State
const loading = ref(true)
const portfolio = ref([])
const categories = ref([])
const showCreateModal = ref(false)
const showEditModal = ref(false)
const showDeleteModal = ref(false)
const editingProject = ref(null)
const deletingProject = ref(null)

// Filters
const filters = ref({
  search: '',
  category: '',
  status: ''
})

// Computed
const filteredPortfolio = computed(() => {
  let filtered = portfolio.value

  // Search filter
  if (filters.value.search) {
    const searchTerm = filters.value.search.toLowerCase()
    filtered = filtered.filter(project =>
      project.title.toLowerCase().includes(searchTerm) ||
      project.description.toLowerCase().includes(searchTerm) ||
      project.category?.name.toLowerCase().includes(searchTerm)
    )
  }

  // Category filter
  if (filters.value.category) {
    filtered = filtered.filter(project => 
      project.category?.id === parseInt(filters.value.category)
    )
  }

  // Status filter
  if (filters.value.status !== '') {
    const isActive = filters.value.status === 'true'
    filtered = filtered.filter(project => project.is_active === isActive)
  }

  return filtered
})

// Methods
const fetchPortfolio = async () => {
  try {
    loading.value = true
    const response = await api.get('/portfolio/admin/projects/')
    portfolio.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to fetch portfolio:', error)
    portfolio.value = []
  } finally {
    loading.value = false
  }
}

const fetchCategories = async () => {
  try {
    const response = await api.get('/portfolio/admin/categories/')
    categories.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to fetch categories:', error)
    categories.value = []
  }
}

const editProject = (project) => {
  editingProject.value = { ...project }
  showEditModal.value = true
}

const deleteProject = (project) => {
  deletingProject.value = project
  showDeleteModal.value = true
}

const confirmDelete = async () => {
  try {
    await api.delete(`/portfolio/admin/projects/${deletingProject.value.id}/`)
    portfolio.value = portfolio.value.filter(p => p.id !== deletingProject.value.id)
    showDeleteModal.value = false
    deletingProject.value = null
  } catch (error) {
    console.error('Failed to delete project:', error)
  }
}

const toggleProjectStatus = async (project) => {
  try {
    const updatedProject = { ...project, is_active: !project.is_active }
    await api.patch(`/portfolio/admin/projects/${project.id}/`, { is_active: updatedProject.is_active })
    
    // Update local state
    const index = portfolio.value.findIndex(p => p.id === project.id)
    if (index !== -1) {
      portfolio.value[index] = updatedProject
    }
  } catch (error) {
    console.error('Failed to update project status:', error)
  }
}

const handleSaveProject = async (projectData) => {
  try {
    if (editingProject.value?.id) {
      // Update existing project
      const response = await api.patch(`/portfolio/admin/projects/${editingProject.value.id}/`, projectData)
      const index = portfolio.value.findIndex(p => p.id === editingProject.value.id)
      if (index !== -1) {
        portfolio.value[index] = response.data
      }
    } else {
      // Create new project
      const response = await api.post('/portfolio/admin/projects/', projectData)
      portfolio.value.unshift(response.data)
    }
    closeModal()
  } catch (error) {
    console.error('Failed to save project:', error)
    throw error
  }
}

const closeModal = () => {
  showCreateModal.value = false
  showEditModal.value = false
  editingProject.value = null
}

const truncateText = (text, maxLength) => {
  if (!text) return ''
  return text.length > maxLength ? text.substring(0, maxLength) + '...' : text
}

const formatDate = (dateString) => {
  if (!dateString) return ''
  return new Date(dateString).toLocaleDateString()
}

// Lifecycle
onMounted(() => {
  fetchPortfolio()
  fetchCategories()
})
</script>