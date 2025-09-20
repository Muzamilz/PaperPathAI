<template>
  <teleport to="body">
    <div class="fixed top-4 right-4 z-50 space-y-2">
      <transition-group
        name="notification"
        tag="div"
        class="space-y-2"
      >
        <div
          v-for="notification in notifications"
          :key="notification.id"
          :class="[
            'notification',
            `notification-${notification.type}`,
            'animate-fade-in-right'
          ]"
        >
          <div class="flex items-start">
            <div class="flex-shrink-0">
              <component :is="getIcon(notification.type)" class="w-5 h-5" :class="getIconColor(notification.type)" />
            </div>
            <div class="ml-3 flex-1">
              <p class="text-sm font-medium text-gray-900">{{ notification.title }}</p>
              <p v-if="notification.message" class="text-sm text-gray-600 mt-1">{{ notification.message }}</p>
            </div>
            <div class="ml-4 flex-shrink-0">
              <button
                @click="removeNotification(notification.id)"
                class="text-gray-400 hover:text-gray-600 transition-colors duration-200"
              >
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                </svg>
              </button>
            </div>
          </div>
          
          <!-- Progress bar for auto-dismiss -->
          <div v-if="notification.autoDismiss" class="mt-2">
            <div class="progress-bar h-1">
              <div 
                class="progress-fill h-full"
                :class="getProgressColor(notification.type)"
                :style="{ width: `${notification.progress}%` }"
              ></div>
            </div>
          </div>
        </div>
      </transition-group>
    </div>
  </teleport>
</template>

<script setup>
import { ref, onMounted, onUnmounted, h } from 'vue'

const notifications = ref([])
let notificationId = 0

// Icons for different notification types
const getIcon = (type) => {
  const icons = {
    success: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z' })
    ]),
    error: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
    ]),
    warning: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-2.5L13.732 4c-.77-.833-1.964-.833-2.732 0L3.34 16.5c-.77.833.192 2.5 1.732 2.5z' })
    ]),
    info: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z' })
    ])
  }
  return icons[type] || icons.info
}

const getIconColor = (type) => {
  const colors = {
    success: 'text-green-600',
    error: 'text-red-600',
    warning: 'text-yellow-600',
    info: 'text-blue-600'
  }
  return colors[type] || colors.info
}

const getProgressColor = (type) => {
  const colors = {
    success: 'bg-green-500',
    error: 'bg-red-500',
    warning: 'bg-yellow-500',
    info: 'bg-blue-500'
  }
  return colors[type] || colors.info
}

const addNotification = (notification) => {
  const id = ++notificationId
  const newNotification = {
    id,
    type: 'info',
    autoDismiss: true,
    duration: 5000,
    progress: 100,
    ...notification
  }
  
  notifications.value.push(newNotification)
  
  if (newNotification.autoDismiss) {
    const startTime = Date.now()
    const interval = setInterval(() => {
      const elapsed = Date.now() - startTime
      const progress = Math.max(0, 100 - (elapsed / newNotification.duration) * 100)
      
      const notificationIndex = notifications.value.findIndex(n => n.id === id)
      if (notificationIndex !== -1) {
        notifications.value[notificationIndex].progress = progress
        
        if (progress <= 0) {
          removeNotification(id)
          clearInterval(interval)
        }
      } else {
        clearInterval(interval)
      }
    }, 50)
  }
  
  return id
}

const removeNotification = (id) => {
  const index = notifications.value.findIndex(n => n.id === id)
  if (index !== -1) {
    notifications.value.splice(index, 1)
  }
}

// Global notification methods
const showSuccess = (title, message = '', options = {}) => {
  return addNotification({ type: 'success', title, message, ...options })
}

const showError = (title, message = '', options = {}) => {
  return addNotification({ type: 'error', title, message, ...options })
}

const showWarning = (title, message = '', options = {}) => {
  return addNotification({ type: 'warning', title, message, ...options })
}

const showInfo = (title, message = '', options = {}) => {
  return addNotification({ type: 'info', title, message, ...options })
}

// Expose methods globally
onMounted(() => {
  window.$notify = {
    success: showSuccess,
    error: showError,
    warning: showWarning,
    info: showInfo,
    remove: removeNotification
  }
})

onUnmounted(() => {
  if (window.$notify) {
    delete window.$notify
  }
})

// Expose methods to parent components
defineExpose({
  showSuccess,
  showError,
  showWarning,
  showInfo,
  removeNotification
})
</script>

<style scoped>
.notification-enter-active,
.notification-leave-active {
  transition: all 0.3s ease;
}

.notification-enter-from {
  opacity: 0;
  transform: translateX(100%);
}

.notification-leave-to {
  opacity: 0;
  transform: translateX(100%);
}

.notification-move {
  transition: transform 0.3s ease;
}
</style>