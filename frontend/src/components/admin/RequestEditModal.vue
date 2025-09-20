<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('close')"></div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-2xl sm:w-full">
        <form @submit.prevent="handleSave">
          <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
            <div class="sm:flex sm:items-start">
              <div class="w-full">
                <!-- Header -->
                <div class="flex items-center justify-between mb-6">
                  <h3 class="text-lg leading-6 font-medium text-gray-900">
                    {{ $t('common.edit') }} {{ $t('admin.request') }}
                  </h3>
                  <button
                    type="button"
                    @click="$emit('close')"
                    class="text-gray-400 hover:text-gray-600"
                  >
                    <svg class="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                      <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
                    </svg>
                  </button>
                </div>

                <!-- Form Fields -->
                <div v-if="editableRequest" class="space-y-4">
                  <div>
                    <label class="block text-sm font-medium text-gray-700">{{ $t('portfolio.projectTitle') }}</label>
                    <input
                      v-model="editableRequest.project_title"
                      type="text"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">{{ $t('admin.status') }}</label>
                    <select
                      v-model="editableRequest.status"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    >
                      <option value="pending">{{ $t('admin.pending') }}</option>
                      <option value="in_progress">{{ $t('admin.inProgress') }}</option>
                      <option value="completed">{{ $t('admin.completed') }}</option>
                      <option value="cancelled">{{ $t('admin.cancelled') }}</option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">{{ $t('admin.priority') }}</label>
                    <select
                      v-model="editableRequest.priority"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    >
                      <option value="low">{{ $t('admin.low') }}</option>
                      <option value="normal">{{ $t('admin.normal') }}</option>
                      <option value="high">{{ $t('admin.high') }}</option>
                      <option value="urgent">{{ $t('admin.urgent') }}</option>
                    </select>
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">{{ $t('admin.deadline') }}</label>
                    <input
                      v-model="editableRequest.deadline"
                      type="date"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    />
                  </div>

                  <div>
                    <label class="block text-sm font-medium text-gray-700">{{ $t('portfolio.projectDescription') }}</label>
                    <textarea
                      v-model="editableRequest.project_description"
                      rows="4"
                      class="mt-1 block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm"
                    ></textarea>
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
            <button
              type="submit"
              :disabled="saving"
              class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm disabled:opacity-50"
            >
              {{ saving ? $t('common.submitting') : $t('common.save') }}
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
import { ref, watch } from 'vue'
import api from '@/utils/api'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  },
  request: {
    type: Object,
    default: null
  }
})

const emit = defineEmits(['close', 'save'])

const editableRequest = ref(null)
const saving = ref(false)

watch(() => props.request, (newRequest) => {
  if (newRequest) {
    editableRequest.value = { ...newRequest }
  }
}, { immediate: true })

const handleSave = async () => {
  if (!editableRequest.value) return

  try {
    saving.value = true
    const response = await api.patch(`/requests/admin/requests/${editableRequest.value.id}/`, editableRequest.value)
    emit('save', response.data)
  } catch (error) {
    console.error('Failed to update request:', error)
  } finally {
    saving.value = false
  }
}
</script>