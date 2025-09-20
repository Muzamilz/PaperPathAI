<template>
  <div v-if="show" class="fixed inset-0 z-50 overflow-y-auto">
    <div class="flex items-end justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity" @click="$emit('close')"></div>

      <span class="hidden sm:inline-block sm:align-middle sm:h-screen">&#8203;</span>

      <div class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full">
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="sm:flex sm:items-start">
            <div class="w-full">
              <!-- Header -->
              <div class="flex items-center justify-between mb-6">
                <h3 class="text-lg leading-6 font-medium text-gray-900">
                  {{ $t('admin.requestsPage.requestDetails') }}
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

              <!-- Request Info -->
              <div v-if="request" class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div>
                  <h4 class="text-sm font-medium text-gray-900 mb-2">{{ $t('admin.requestsPage.requestDetails') }}</h4>
                  <div class="bg-gray-50 p-4 rounded-lg space-y-2">
                    <div>
                      <span class="text-sm font-medium text-gray-500">ID:</span>
                      <span class="text-sm text-gray-900 ml-2">#{{ request.id }}</span>
                    </div>
                    <div>
                      <span class="text-sm font-medium text-gray-500">{{ $t('portfolio.projectTitle') }}:</span>
                      <span class="text-sm text-gray-900 ml-2">{{ request.project_title }}</span>
                    </div>
                    <div>
                      <span class="text-sm font-medium text-gray-500">{{ $t('admin.status') }}:</span>
                      <span class="text-sm text-gray-900 ml-2">{{ $t('admin.' + request.status) }}</span>
                    </div>
                    <div>
                      <span class="text-sm font-medium text-gray-500">{{ $t('admin.priority') }}:</span>
                      <span class="text-sm text-gray-900 ml-2">{{ $t('admin.' + request.priority) }}</span>
                    </div>
                  </div>
                </div>

                <div>
                  <h4 class="text-sm font-medium text-gray-900 mb-2">{{ $t('admin.requestsPage.clientInfo') }}</h4>
                  <div class="bg-gray-50 p-4 rounded-lg space-y-2">
                    <div>
                      <span class="text-sm font-medium text-gray-500">{{ $t('contact.name') }}:</span>
                      <span class="text-sm text-gray-900 ml-2">{{ request.client_name }}</span>
                    </div>
                    <div>
                      <span class="text-sm font-medium text-gray-500">{{ $t('contact.email') }}:</span>
                      <span class="text-sm text-gray-900 ml-2">{{ request.client_email }}</span>
                    </div>
                    <div v-if="request.client_phone">
                      <span class="text-sm font-medium text-gray-500">{{ $t('contact.phone') }}:</span>
                      <span class="text-sm text-gray-900 ml-2">{{ request.client_phone }}</span>
                    </div>
                  </div>
                </div>

                <div class="md:col-span-2">
                  <h4 class="text-sm font-medium text-gray-900 mb-2">{{ $t('portfolio.projectDescription') }}</h4>
                  <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-900">{{ request.project_description || $t('admin.noDescription') }}</p>
                  </div>
                </div>

                <div v-if="request.service" class="md:col-span-2">
                  <h4 class="text-sm font-medium text-gray-900 mb-2">{{ $t('admin.service') }}</h4>
                  <div class="bg-gray-50 p-4 rounded-lg">
                    <p class="text-sm text-gray-900">{{ request.service.title }}</p>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            @click="$emit('close')"
            type="button"
            class="w-full inline-flex justify-center rounded-md border border-gray-300 shadow-sm px-4 py-2 bg-white text-base font-medium text-gray-700 hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
          >
            {{ $t('common.close') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  show: {
    type: Boolean,
    default: false
  },
  request: {
    type: Object,
    default: null
  }
})

defineEmits(['close', 'update'])
</script>