<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('close')"></div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-lg sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="w-full">
              <!-- Header -->
              <div class="flex items-center justify-between mb-6">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  {{ $t('admin.bulkActions') }}
                </h3>
                <button
                  @click="$emit('close')"
                  class="text-gray-400 hover:text-gray-600"
                >
                  <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                  </svg>
                </button>
              </div>

              <p class="text-sm text-gray-500 mb-4">
                {{ selectedCount }} {{ $t('admin.requests') }} selected
              </p>

              <!-- Action Selection -->
              <div class="space-y-4">
                <div>
                  <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('admin.actions') }}</label>
                  <select
                    v-model="selectedAction"
                    class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                  >
                    <option value="">{{ $t('admin.selectAction') }}</option>
                    <option value="update_status">{{ $t('admin.requestsPage.updateStatus') }}</option>
                    <option value="update_priority">{{ $t('admin.updatePriority') }}</option>
                    <option value="delete">{{ $t('common.delete') }}</option>
                  </select>
                </div>

                <!-- Status Update -->
                <div v-if="selectedAction === 'update_status'">
                  <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('admin.status') }}</label>
                  <select
                    v-model="actionData.status"
                    class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                  >
                    <option value="pending">{{ $t('admin.pending') }}</option>
                    <option value="in_progress">{{ $t('admin.inProgress') }}</option>
                    <option value="completed">{{ $t('admin.completed') }}</option>
                    <option value="cancelled">{{ $t('admin.cancelled') }}</option>
                  </select>
                </div>

                <!-- Priority Update -->
                <div v-if="selectedAction === 'update_priority'">
                  <label class="block text-sm font-medium text-gray-700 mb-2">{{ $t('admin.priority') }}</label>
                  <select
                    v-model="actionData.priority"
                    class="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                  >
                    <option value="low">{{ $t('admin.low') }}</option>
                    <option value="normal">{{ $t('admin.normal') }}</option>
                    <option value="high">{{ $t('admin.high') }}</option>
                    <option value="urgent">{{ $t('admin.urgent') }}</option>
                  </select>
                </div>

                <!-- Delete Confirmation -->
                <div v-if="selectedAction === 'delete'" class="bg-red-50 p-4 rounded-md">
                  <div class="flex">
                    <div class="flex-shrink-0">
                      <svg class="h-5 w-5 text-red-400" fill="currentColor" viewBox="0 0 20 20">
                        <path fill-rule="evenodd" d="M8.257 3.099c.765-1.36 2.722-1.36 3.486 0l5.58 9.92c.75 1.334-.213 2.98-1.742 2.98H4.42c-1.53 0-2.493-1.646-1.743-2.98l5.58-9.92zM11 13a1 1 0 11-2 0 1 1 0 012 0zm-1-8a1 1 0 00-1 1v3a1 1 0 002 0V6a1 1 0 00-1-1z" clip-rule="evenodd" />
                      </svg>
                    </div>
                    <div class="ml-3">
                      <h3 class="text-sm font-medium text-red-800">
                        {{ $t('admin.warning') }}
                      </h3>
                      <div class="mt-2 text-sm text-red-700">
                        <p>{{ $t('admin.deleteWarning') }}</p>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            @click="handleAction"
            :disabled="!selectedAction || processing"
            :class="[
              'w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 text-base font-medium text-white focus:outline-none focus:ring-2 focus:ring-offset-2 sm:ml-3 sm:w-auto sm:text-sm',
              selectedAction === 'delete' 
                ? 'bg-red-600 hover:bg-red-700 focus:ring-red-500' 
                : 'bg-blue-600 hover:bg-blue-700 focus:ring-blue-500',
              (!selectedAction || processing) && 'opacity-50 cursor-not-allowed'
            ]"
          >
            {{ processing ? $t('admin.processing') : $t('admin.applyAction') }}
          </button>
          <button
            @click="$emit('close')"
            type="button"
            class="mt-3 w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:mt-0 sm:ml-3 sm:w-auto sm:text-sm"
          >
            {{ $t('common.cancel') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive } from 'vue'

defineProps({
  show: {
    type: Boolean,
    default: false
  },
  selectedCount: {
    type: Number,
    default: 0
  }
})

const emit = defineEmits(['close', 'action'])

const selectedAction = ref('')
const processing = ref(false)
const actionData = reactive({
  status: '',
  priority: ''
})

const handleAction = () => {
  if (!selectedAction.value) return

  processing.value = true
  
  const action = {
    type: selectedAction.value,
    data: actionData
  }

  emit('action', action)
  
  // Reset form
  selectedAction.value = ''
  actionData.status = ''
  actionData.priority = ''
  processing.value = false
}
</script>