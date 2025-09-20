<template>
  <div class="fixed inset-0 z-50 overflow-y-auto" @click="$emit('close')">
    <div class="flex items-center justify-center min-h-screen pt-4 px-4 pb-20 text-center sm:block sm:p-0">
      <!-- Background overlay -->
      <div class="fixed inset-0 bg-gray-500 bg-opacity-75 transition-opacity"></div>

      <!-- Modal panel -->
      <div 
        class="inline-block align-bottom bg-white rounded-lg text-left overflow-hidden shadow-xl transform transition-all sm:my-8 sm:align-middle sm:max-w-4xl sm:w-full"
        @click.stop
      >
        <!-- Modal header -->
        <div class="bg-white px-4 pt-5 pb-4 sm:p-6 sm:pb-4">
          <div class="flex items-center justify-between mb-4">
            <h3 class="text-lg leading-6 font-medium text-gray-900">
              {{ item.title }}
            </h3>
            <button
              @click="$emit('close')"
              class="rounded-md text-gray-400 hover:text-gray-600 focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <svg class="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12" />
              </svg>
            </button>
          </div>

          <!-- Meta information -->
          <div class="flex flex-wrap items-center gap-4 text-sm text-gray-600 mb-6">
            <span class="flex items-center">
              <svg class="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 7h.01M7 3h5c.512 0 1.024.195 1.414.586l7 7a2 2 0 010 2.828l-7 7a2 2 0 01-2.828 0l-7-7A1.994 1.994 0 013 12V7a4 4 0 014-4z" />
              </svg>
              {{ item.service_category?.name }}
            </span>
            <span class="flex items-center">
              <svg class="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 7V3m8 4V3m-9 8h10M5 21h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v12a2 2 0 002 2z" />
              </svg>
              {{ $t('portfolio.completedOn') }}: {{ formatDate(item.completion_date) }}
            </span>
            <span class="flex items-center">
              <svg class="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M16 7a4 4 0 11-8 0 4 4 0 018 0zM12 14a7 7 0 00-7 7h14a7 7 0 00-7-7z" />
              </svg>
              {{ item.client_type }}
            </span>
          </div>
        </div>

        <!-- Modal content -->
        <div class="bg-white px-4 pb-4 sm:p-6 sm:pt-0">
          <!-- Image -->
          <div v-if="item.image" class="mb-6">
            <img 
              :src="item.image" 
              :alt="item.title"
              class="w-full h-64 sm:h-80 object-cover rounded-lg shadow-md"
            />
          </div>

          <!-- Description -->
          <div class="mb-6">
            <h4 class="text-lg font-semibold mb-3">{{ $t('portfolio.projectDescription') }}</h4>
            <div class="prose max-w-none text-gray-700">
              <p>{{ item.description }}</p>
            </div>
          </div>

          <!-- Technologies Used -->
          <div v-if="item.technologies_used && item.technologies_used.length" class="mb-6">
            <h4 class="text-lg font-semibold mb-3">{{ $t('portfolio.technologies') }}</h4>
            <div class="flex flex-wrap gap-2">
              <span 
                v-for="tech in item.technologies_used" 
                :key="tech"
                class="px-3 py-1 bg-blue-100 text-blue-800 rounded-full text-sm font-medium"
              >
                {{ tech }}
              </span>
            </div>
          </div>

          <!-- Featured badge -->
          <div v-if="item.is_featured" class="mb-4">
            <span class="inline-flex items-center px-3 py-1 rounded-full text-sm font-medium bg-yellow-100 text-yellow-800">
              <svg class="w-4 h-4 mr-1 rtl:mr-0 rtl:ml-1" fill="currentColor" viewBox="0 0 20 20">
                <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
              </svg>
              {{ $t('portfolio.featured') }}
            </span>
          </div>
        </div>

        <!-- Modal footer -->
        <div class="bg-gray-50 px-4 py-3 sm:px-6 sm:flex sm:flex-row-reverse">
          <button
            @click="$emit('close')"
            type="button"
            class="w-full inline-flex justify-center rounded-md border border-transparent shadow-sm px-4 py-2 bg-blue-600 text-base font-medium text-white hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 sm:ml-3 sm:w-auto sm:text-sm"
          >
            {{ $t('common.close') }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, onUnmounted } from 'vue'
import { useLanguageStore } from '@/stores/language'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['close'])

const languageStore = useLanguageStore()

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString(languageStore.currentLanguage === 'ar' ? 'ar-SA' : 'en-US')
}

// Close modal on escape key
const handleKeydown = (event) => {
  if (event.key === 'Escape') {
    emit('close')
  }
}

// Add event listener when component mounts
onMounted(() => {
  document.addEventListener('keydown', handleKeydown)
})

// Remove event listener when component unmounts
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeydown)
})
</script>

<style scoped>
.prose p {
  @apply mb-4 leading-relaxed;
}
</style>