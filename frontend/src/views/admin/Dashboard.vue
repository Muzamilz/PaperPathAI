<template>
  <div class="px-4 sm:px-6 lg:px-8">
    <!-- Page Header -->
    <div class="sm:flex sm:items-center">
      <div class="sm:flex-auto">
        <h1 class="text-2xl font-semibold text-gray-900">{{ $t('admin.dashboard') }}</h1>
        <p class="mt-2 text-sm text-gray-700">
          {{ $t('admin.dashboard.overview') }}
        </p>
      </div>
    </div>

    <!-- Stats Grid -->
    <div class="mt-8 grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
      <!-- Total Services -->
      <div class="card-elevated p-6 group hover:scale-105 transition-all duration-300">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600 mb-1">{{ $t('admin.totalServices') }}</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.totalServices }}</p>
            <div class="flex items-center mt-2">
              <span class="text-xs text-green-600 font-medium bg-green-100 px-2 py-1 rounded-full">
                +12% from last month
              </span>
            </div>
          </div>
          <div class="w-12 h-12 bg-gradient-to-br from-blue-500 to-blue-600 rounded-2xl flex items-center justify-center group-hover:rotate-6 transition-transform duration-300">
            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Pending Requests -->
      <div class="card-elevated p-6 group hover:scale-105 transition-all duration-300">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600 mb-1">{{ $t('admin.pendingRequests') }}</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.pendingRequests }}</p>
            <div class="flex items-center mt-2">
              <span class="text-xs text-yellow-600 font-medium bg-yellow-100 px-2 py-1 rounded-full">
                Needs attention
              </span>
            </div>
          </div>
          <div class="w-12 h-12 bg-gradient-to-br from-yellow-500 to-yellow-600 rounded-2xl flex items-center justify-center group-hover:rotate-6 transition-transform duration-300">
            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Active Requests -->
      <div class="card-elevated p-6 group hover:scale-105 transition-all duration-300">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600 mb-1">{{ $t('admin.requestsPage.activeRequests') }}</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.activeRequests }}</p>
            <div class="flex items-center mt-2">
              <span class="text-xs text-green-600 font-medium bg-green-100 px-2 py-1 rounded-full">
                On track
              </span>
            </div>
          </div>
          <div class="w-12 h-12 bg-gradient-to-br from-green-500 to-green-600 rounded-2xl flex items-center justify-center group-hover:rotate-6 transition-transform duration-300">
            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z" />
            </svg>
          </div>
        </div>
      </div>

      <!-- Portfolio Items -->
      <div class="card-elevated p-6 group hover:scale-105 transition-all duration-300">
        <div class="flex items-center justify-between">
          <div class="flex-1">
            <p class="text-sm font-medium text-gray-600 mb-1">{{ $t('admin.portfolioPage.portfolioItems') }}</p>
            <p class="text-3xl font-bold text-gray-900">{{ stats.portfolioItems }}</p>
            <div class="flex items-center mt-2">
              <span class="text-xs text-purple-600 font-medium bg-purple-100 px-2 py-1 rounded-full">
                Showcase ready
              </span>
            </div>
          </div>
          <div class="w-12 h-12 bg-gradient-to-br from-purple-500 to-purple-600 rounded-2xl flex items-center justify-center group-hover:rotate-6 transition-transform duration-300">
            <svg class="h-6 w-6 text-white" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z" />
            </svg>
          </div>
        </div>
      </div>
    </div>

    <!-- Recent Activity -->
    <div class="mt-8">
      <div class="bg-white shadow rounded-lg">
        <div class="px-4 py-5 sm:p-6">
          <h3 class="text-lg leading-6 font-medium text-gray-900 mb-4">{{ $t('admin.recentActivity') }}</h3>
          
          <div v-if="loading" class="text-center py-4">
            <div class="animate-spin rounded-full h-8 w-8 border-b-2 border-blue-600 mx-auto"></div>
            <p class="mt-2 text-sm text-gray-500">{{ $t('common.loading') }}</p>
          </div>
          
          <div v-else-if="recentActivity.length === 0" class="text-center py-8">
            <svg class="mx-auto h-12 w-12 text-gray-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2" />
            </svg>
            <h3 class="mt-2 text-sm font-medium text-gray-900">{{ $t('admin.noData') }}</h3>
            <p class="mt-1 text-sm text-gray-500">{{ $t('admin.dashboard.recentActivityDescription') }}</p>
          </div>
          
          <div v-else class="flow-root">
            <ul class="-mb-8">
              <li v-for="(activity, index) in recentActivity" :key="activity.id" class="relative pb-8">
                <div v-if="index !== recentActivity.length - 1" class="absolute top-4 left-4 -ml-px h-full w-0.5 bg-gray-200"></div>
                <div class="relative flex space-x-3">
                  <div>
                    <span class="h-8 w-8 rounded-full flex items-center justify-center ring-8 ring-white"
                          :class="getActivityIconClass(activity.type)">
                      <component :is="getActivityIcon(activity.type)" class="h-4 w-4 text-white" />
                    </span>
                  </div>
                  <div class="min-w-0 flex-1 pt-1.5 flex justify-between space-x-4">
                    <div>
                      <p class="text-sm text-gray-500">{{ activity.description }}</p>
                    </div>
                    <div class="text-right text-sm whitespace-nowrap text-gray-500">
                      {{ formatDate(activity.created_at) }}
                    </div>
                  </div>
                </div>
              </li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, h } from 'vue'
import api from '@/utils/api'

// State
const loading = ref(true)
const stats = ref({
  totalServices: 0,
  pendingRequests: 0,
  activeRequests: 0,
  portfolioItems: 0
})
const recentActivity = ref([])

// Methods
const fetchDashboardData = async () => {
  try {
    loading.value = true
    const response = await api.get('/dashboard/stats/')
    stats.value = response.data.stats
    recentActivity.value = response.data.recent_activity || []
  } catch (error) {
    console.error('Failed to fetch dashboard data:', error)
    // Set default values on error
    stats.value = {
      totalServices: 0,
      pendingRequests: 0,
      activeRequests: 0,
      portfolioItems: 0
    }
    recentActivity.value = []
  } finally {
    loading.value = false
  }
}

const getActivityIconClass = (type) => {
  const classes = {
    'request': 'bg-blue-500',
    'service': 'bg-green-500',
    'portfolio': 'bg-purple-500',
    'default': 'bg-gray-500'
  }
  return classes[type] || classes.default
}

const getActivityIcon = (type) => {
  const icons = {
    'request': () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2' })
    ]),
    'service': () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10' })
    ]),
    'portfolio': () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M19 11a7 7 0 01-7 7m0 0a7 7 0 01-7-7m7 7v4m0 0H8m4 0h4m-4-8a3 3 0 01-3-3V5a3 3 0 116 0v6a3 3 0 01-3 3z' })
    ])
  }
  return icons[type] || icons.request
}

const formatDate = (dateString) => {
  const date = new Date(dateString)
  const now = new Date()
  const diffInHours = Math.floor((now - date) / (1000 * 60 * 60))
  
  if (diffInHours < 1) {
    return 'Just now'
  } else if (diffInHours < 24) {
    return `${diffInHours}h ago`
  } else {
    const diffInDays = Math.floor(diffInHours / 24)
    return `${diffInDays}d ago`
  }
}

// Lifecycle
onMounted(() => {
  fetchDashboardData()
})
</script>