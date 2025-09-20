<template>
  <div class="px-4 sm:px-6 lg:px-8">
    <!-- Page Header -->
    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <h1 class="text-2xl font-semibold text-gray-900">{{ $t('admin.requests') }}</h1>
        <p class="mt-2 text-sm text-gray-700">
          {{ $t('admin.requestsPage.manageRequests') }}
        </p>
      </div>
      <div class="mt-4 sm:mt-0 sm:ml-16 sm:flex-none">
        <div class="flex space-x-2">
          <button
            @click="refreshRequests"
            :disabled="loading"
            class="inline-flex items-center justify-center rounded-md border border-gray-300 bg-white px-4 py-2 text-sm font-medium text-gray-700 shadow-sm hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 disabled:opacity-50"
          >
            <svg class="-ml-1 mr-2 h-5 w-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15" />
            </svg>
            {{ $t('common.retry') }}
          </button>
          <button
            v-if="selectedRequests.length > 0"
            @click="showBulkActionsModal = true"
            class="inline-flex items-center justify-center rounded-md border border-transparent bg-blue-600 px-4 py-2 text-sm font-medium text-white shadow-sm hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2"
          >
            {{ $t('admin.bulkActions') }} ({{ selectedRequests.length }})
          </button>
        </div>
      </div>
    </div>

    <!-- Filters and Search -->
    <div class="mt-6 bg-white shadow rounded-lg p-4">
      <div class="grid grid-cols-1 gap-4 sm:grid-cols-4">
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

        <!-- Status Filter -->
        <div>
          <label for="status" class="block text-sm font-medium text-gray-700">{{ $t('admin.status') }}</label>
          <select
            id="status"
            v-model="filters.status"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          >
            <option value="">{{ $t('admin.allStatus') }}</option>
            <option value="pending">{{ $t('admin.pending') }}</option>
            <option value="in_progress">{{ $t('admin.inProgress') }}</option>
            <option value="completed">{{ $t('admin.completed') }}</option>
            <option value="cancelled">{{ $t('admin.cancelled') }}</option>
          </select>
        </div>

        <!-- Priority Filter -->
        <div>
          <label for="priority" class="block text-sm font-medium text-gray-700">{{ $t('admin.priority') }}</label>
          <select
            id="priority"
            v-model="filters.priority"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          >
            <option value="">{{ $t('admin.allPriorities') }}</option>
            <option value="low">{{ $t('admin.low') }}</option>
            <option value="normal">{{ $t('admin.normal') }}</option>
            <option value="high">{{ $t('admin.high') }}</option>
            <option value="urgent">{{ $t('admin.urgent') }}</option>
          </select>
        </div>

        <!-- Assigned Filter -->
        <div>
          <label for="assigned" class="block text-sm font-medium text-gray-700">{{ $t('admin.requestsPage.assignTo') }}</label>
          <select
            id="assigned"
            v-model="filters.assigned"
            class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
          >
            <option value="">{{ $t('admin.allAssignments') }}</option>
            <option value="unassigned">{{ $t('admin.unassigned') }}</option>
            <option value="me">{{ $t('admin.assignedToMe') }}</option>
          </select>
        </div>
      </div>
    </div>

    <!-- Requests Table -->
    <div class="mt-6 bg-white shadow rounded-lg overflow-hidden">
      <div v-if="loading" class="space-y-4">
        <!-- Skeleton Loading -->
        <div class="card p-6">
          <div class="flex items-center justify-between mb-4">
            <div class="skeleton-title"></div>
            <div class="skeleton-button"></div>
          </div>
          <div class="grid grid-cols-4 gap-4 mb-4">
            <div class="skeleton-text"></div>
            <div class="skeleton-text"></div>
            <div class="skeleton-text"></div>
            <div class="skeleton-text"></div>
          </div>
        </div>
        
        <!-- Table Skeleton -->
        <div class="card overflow-hidden">
          <div class="p-4 border-b border-gray-200">
            <div class="skeleton-title w-1/4"></div>
          </div>
          <div class="divide-y divide-gray-200">
            <div v-for="i in 5" :key="i" class="p-4 flex items-center space-x-4">
              <div class="skeleton w-4 h-4"></div>
              <div class="flex-1 space-y-2">
                <div class="skeleton-text w-3/4"></div>
                <div class="skeleton-text w-1/2"></div>
              </div>
              <div class="skeleton w-20 h-6 rounded-full"></div>
              <div class="skeleton w-16 h-6 rounded-full"></div>
              <div class="skeleton-button"></div>
            </div>
          </div>
        </div>
      </div>

      <div v-else-if="filteredRequests.length === 0" class="text-center py-12">
        <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
        </svg>
        <h3 class="mt-2 text-sm font-medium text-gray-900">{{ $t('admin.noRequestsFound') }}</h3>
        <p class="mt-1 text-sm text-gray-500">{{ $t('admin.noRequestsDescription') }}</p>
      </div>

      <div v-else class="overflow-x-auto">
        <table class="min-w-full divide-y divide-gray-200">
          <thead class="bg-gray-50">
            <tr>
              <th class="px-6 py-3 text-left">
                <input
                  type="checkbox"
                  :checked="allSelected"
                  @change="toggleSelectAll"
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('admin.request') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('admin.client') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('admin.service') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('admin.status') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('admin.priority') }}
              </th>
              <th class="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider">
                {{ $t('admin.deadline') }}
              </th>
              <th class="relative px-6 py-3">
                <span class="sr-only">Actions</span>
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-gray-200">
            <tr v-for="request in filteredRequests" :key="request.id" class="hover:bg-gray-50">
              <td class="px-6 py-4 whitespace-nowrap">
                <input
                  type="checkbox"
                  :checked="selectedRequests.includes(request.id)"
                  @change="toggleSelectRequest(request.id)"
                  class="h-4 w-4 text-blue-600 focus:ring-blue-500 border-gray-300 rounded"
                />
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="flex items-center">
                  <div>
                    <div class="text-sm font-medium text-gray-900">{{ request.project_title }}</div>
                    <div class="text-sm text-gray-500">ID: #{{ request.id }}</div>
                  </div>
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ request.client_name }}</div>
                <div class="text-sm text-gray-500">{{ request.client_email }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <div class="text-sm text-gray-900">{{ request.service?.title || 'N/A' }}</div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <select
                  :value="request.status"
                  @change="updateRequestStatus(request, $event.target.value)"
                  :class="getStatusClass(request.status)"
                  class="text-xs font-medium rounded-full px-2.5 py-0.5 border-0 focus:ring-2 focus:ring-blue-500"
                >
                  <option value="pending">{{ $t('admin.pending') }}</option>
                  <option value="in_progress">{{ $t('admin.inProgress') }}</option>
                  <option value="completed">{{ $t('admin.completed') }}</option>
                  <option value="cancelled">{{ $t('admin.cancelled') }}</option>
                </select>
              </td>
              <td class="px-6 py-4 whitespace-nowrap">
                <select
                  :value="request.priority"
                  @change="updateRequestPriority(request, $event.target.value)"
                  :class="getPriorityClass(request.priority)"
                  class="text-xs font-medium rounded-full px-2.5 py-0.5 border-0 focus:ring-2 focus:ring-blue-500"
                >
                  <option value="low">{{ $t('admin.low') }}</option>
                  <option value="normal">{{ $t('admin.normal') }}</option>
                  <option value="high">{{ $t('admin.high') }}</option>
                  <option value="urgent">{{ $t('admin.urgent') }}</option>
                </select>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-sm text-gray-900">
                <div :class="{ 'text-red-600 font-medium': isOverdue(request.deadline) }">
                  {{ formatDate(request.deadline) }}
                </div>
              </td>
              <td class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
                <div class="flex items-center space-x-2">
                  <button
                    @click="viewRequest(request)"
                    class="text-blue-600 hover:text-blue-900"
                  >
                    {{ $t('admin.view') }}
                  </button>
                  <button
                    @click="editRequest(request)"
                    class="text-green-600 hover:text-green-900"
                  >
                    {{ $t('common.edit') }}
                  </button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Request Detail Modal -->
    <RequestDetailModal
      v-if="showDetailModal"
      :show="showDetailModal"
      :request="selectedRequest"
      @close="showDetailModal = false"
      @update="handleRequestUpdate"
    />

    <!-- Request Edit Modal -->
    <RequestEditModal
      v-if="showEditModal"
      :show="showEditModal"
      :request="editingRequest"
      @close="showEditModal = false"
      @save="handleRequestSave"
    />

    <!-- Bulk Actions Modal -->
    <BulkActionsModal
      v-if="showBulkActionsModal"
      :show="showBulkActionsModal"
      :selected-count="selectedRequests.length"
      @close="showBulkActionsModal = false"
      @action="handleBulkAction"
    />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import api from '@/utils/api'
import RequestDetailModal from '@/components/admin/RequestDetailModal.vue'
import RequestEditModal from '@/components/admin/RequestEditModal.vue'
import BulkActionsModal from '@/components/admin/BulkActionsModal.vue'

const authStore = useAuthStore()

// State
const loading = ref(true)
const requests = ref([])
const selectedRequests = ref([])
const showDetailModal = ref(false)
const showEditModal = ref(false)
const showBulkActionsModal = ref(false)
const selectedRequest = ref(null)
const editingRequest = ref(null)

// Filters
const filters = ref({
  search: '',
  status: '',
  priority: '',
  assigned: ''
})

// Computed
const filteredRequests = computed(() => {
  let filtered = requests.value

  // Search filter
  if (filters.value.search) {
    const searchTerm = filters.value.search.toLowerCase()
    filtered = filtered.filter(request =>
      request.project_title.toLowerCase().includes(searchTerm) ||
      request.client_name.toLowerCase().includes(searchTerm) ||
      request.client_email.toLowerCase().includes(searchTerm) ||
      request.service?.title.toLowerCase().includes(searchTerm)
    )
  }

  // Status filter
  if (filters.value.status) {
    filtered = filtered.filter(request => request.status === filters.value.status)
  }

  // Priority filter
  if (filters.value.priority) {
    filtered = filtered.filter(request => request.priority === filters.value.priority)
  }

  // Assignment filter
  if (filters.value.assigned === 'unassigned') {
    filtered = filtered.filter(request => !request.assigned_to)
  } else if (filters.value.assigned === 'me') {
    filtered = filtered.filter(request => request.assigned_to?.id === authStore.user?.id)
  }

  return filtered
})

const allSelected = computed(() => {
  return filteredRequests.value.length > 0 && 
         selectedRequests.value.length === filteredRequests.value.length
})

// Methods
const fetchRequests = async () => {
  try {
    loading.value = true
    const response = await api.get('/requests/admin/requests/')
    requests.value = response.data.results || response.data
  } catch (error) {
    console.error('Failed to fetch requests:', error)
    requests.value = []
  } finally {
    loading.value = false
  }
}

const refreshRequests = () => {
  fetchRequests()
}

const toggleSelectAll = () => {
  if (allSelected.value) {
    selectedRequests.value = []
  } else {
    selectedRequests.value = filteredRequests.value.map(r => r.id)
  }
}

const toggleSelectRequest = (requestId) => {
  const index = selectedRequests.value.indexOf(requestId)
  if (index > -1) {
    selectedRequests.value.splice(index, 1)
  } else {
    selectedRequests.value.push(requestId)
  }
}

const updateRequestStatus = async (request, newStatus) => {
  try {
    await api.patch(`/requests/admin/requests/${request.id}/`, { status: newStatus })
    
    // Update local state
    const index = requests.value.findIndex(r => r.id === request.id)
    if (index !== -1) {
      requests.value[index].status = newStatus
    }
  } catch (error) {
    console.error('Failed to update request status:', error)
  }
}

const updateRequestPriority = async (request, newPriority) => {
  try {
    await api.patch(`/requests/admin/requests/${request.id}/`, { priority: newPriority })
    
    // Update local state
    const index = requests.value.findIndex(r => r.id === request.id)
    if (index !== -1) {
      requests.value[index].priority = newPriority
    }
  } catch (error) {
    console.error('Failed to update request priority:', error)
  }
}

const viewRequest = (request) => {
  selectedRequest.value = request
  showDetailModal.value = true
}

const editRequest = (request) => {
  editingRequest.value = { ...request }
  showEditModal.value = true
}

const handleRequestUpdate = (updatedRequest) => {
  const index = requests.value.findIndex(r => r.id === updatedRequest.id)
  if (index !== -1) {
    requests.value[index] = updatedRequest
  }
}

const handleRequestSave = (updatedRequest) => {
  const index = requests.value.findIndex(r => r.id === updatedRequest.id)
  if (index !== -1) {
    requests.value[index] = updatedRequest
  }
  showEditModal.value = false
  editingRequest.value = null
}

const handleBulkAction = async (action) => {
  try {
    const payload = {
      request_ids: selectedRequests.value,
      type: action.type,
      data: action.data
    }
    
    await api.post('/requests/admin/requests/bulk_action/', payload)
    
    // Refresh requests after bulk action
    await fetchRequests()
    selectedRequests.value = []
    showBulkActionsModal.value = false
  } catch (error) {
    console.error('Failed to perform bulk action:', error)
  }
}

const getStatusClass = (status) => {
  const classes = {
    'pending': 'bg-yellow-100 text-yellow-800',
    'in_progress': 'bg-blue-100 text-blue-800',
    'completed': 'bg-green-100 text-green-800',
    'cancelled': 'bg-red-100 text-red-800'
  }
  return classes[status] || 'bg-gray-100 text-gray-800'
}

const getPriorityClass = (priority) => {
  const classes = {
    'low': 'bg-gray-100 text-gray-800',
    'normal': 'bg-blue-100 text-blue-800',
    'high': 'bg-orange-100 text-orange-800',
    'urgent': 'bg-red-100 text-red-800'
  }
  return classes[priority] || 'bg-gray-100 text-gray-800'
}

const isOverdue = (deadline) => {
  if (!deadline) return false
  const deadlineDate = new Date(deadline)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return deadlineDate < today
}

const formatDate = (dateString) => {
  if (!dateString) return 'No deadline'
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

// Lifecycle
onMounted(() => {
  fetchRequests()
})
</script>