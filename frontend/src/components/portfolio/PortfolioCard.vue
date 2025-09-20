<template>
  <div class="portfolio-card bg-white rounded-2xl overflow-hidden hover:shadow-lg transition-all duration-200 group">
    <!-- Image with lazy loading -->
    <div class="relative h-64 bg-gradient-to-br from-blue-400 to-blue-600 overflow-hidden">
      <img
        v-if="item.image && (imageLoaded || isInViewport)"
        :src="item.image"
        :alt="item.title"
        @load="onImageLoad"
        @error="onImageError"
        :class="[
          'w-full h-full object-cover transition-all duration-300 group-hover:scale-105',
          imageLoaded ? 'opacity-100' : 'opacity-0'
        ]"
      />
      
      <!-- Default gradient background with icon -->
      <div 
        v-if="!item.image || imageError || (!imageLoaded && !isInViewport)"
        class="absolute inset-0 flex items-center justify-center bg-gradient-to-br from-blue-400 to-blue-600"
      >
        <div class="text-white text-center">
          <svg class="w-16 h-16 mx-auto mb-2 opacity-80" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="1.5" :d="getIconPath(item.category)" />
          </svg>
          <p class="text-sm opacity-75">{{ getCategoryName(item.category) }}</p>
        </div>
      </div>

      <!-- Loading placeholder -->
      <div 
        v-if="item.image && !imageLoaded && !imageError && isInViewport"
        class="absolute inset-0 flex items-center justify-center bg-gray-200"
      >
        <div class="animate-pulse">
          <div class="w-12 h-12 bg-gray-300 rounded-full"></div>
        </div>
      </div>
    </div>

    <!-- Content -->
    <div class="p-6">
      <h3 class="text-lg font-semibold text-gray-900 mb-2 line-clamp-2">
        {{ item.title }}
      </h3>
      
      <p class="text-gray-600 text-sm leading-relaxed line-clamp-3">
        {{ item.description }}
      </p>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
import { useLanguageStore } from '@/stores/language'

const props = defineProps({
  item: {
    type: Object,
    required: true
  }
})

const languageStore = useLanguageStore()

// Reactive state
const imageLoaded = ref(false)
const imageError = ref(false)
const isInViewport = ref(false)
const cardRef = ref(null)

// Intersection Observer for lazy loading
let observer = null

const formatDate = (dateString) => {
  const date = new Date(dateString)
  return date.toLocaleDateString(languageStore.currentLanguage === 'ar' ? 'ar-SA' : 'en-US')
}

const getCategoryName = (category) => {
  if (!category) return 'Project'
  return category.name || 'Project'
}

const getIconPath = (category) => {
  const categoryName = category?.name?.toLowerCase() || ''
  
  if (categoryName.includes('research') || categoryName.includes('literature')) {
    return 'M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.746 0 3.332.477 4.5 1.253v13C19.832 18.477 18.246 18 16.5 18c-1.746 0-3.332.477-4.5 1.253'
  } else if (categoryName.includes('data') || categoryName.includes('analysis')) {
    return 'M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z'
  } else if (categoryName.includes('presentation') || categoryName.includes('design')) {
    return 'M7 4V2a1 1 0 011-1h8a1 1 0 011 1v2m-9 0h10m-10 0a2 2 0 00-2 2v14a2 2 0 002 2h10a2 2 0 002-2V6a2 2 0 00-2-2'
  } else if (categoryName.includes('tutoring') || categoryName.includes('calculus')) {
    return 'M9 7h6m0 10v-3m-3 3h.01M9 17h.01M9 14h.01M12 14h.01M15 11h.01M12 11h.01M9 11h.01M7 21h10a2 2 0 002-2V5a2 2 0 00-2-2H7a2 2 0 00-2 2v14a2 2 0 002 2z'
  } else if (categoryName.includes('case') || categoryName.includes('study')) {
    return 'M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 9a2 2 0 012-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10'
  }
  
  // Default icon
  return 'M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z'
}

const onImageLoad = () => {
  imageLoaded.value = true
}

const onImageError = () => {
  imageError.value = true
}

const setupIntersectionObserver = () => {
  if (!window.IntersectionObserver) {
    isInViewport.value = true
    return
  }

  observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          isInViewport.value = true
          observer.unobserve(entry.target)
        }
      })
    },
    {
      rootMargin: '50px'
    }
  )

  if (cardRef.value) {
    observer.observe(cardRef.value)
  }
}

onMounted(() => {
  setupIntersectionObserver()
})

onUnmounted(() => {
  if (observer) {
    observer.disconnect()
  }
})
</script>

<style scoped>
.line-clamp-2 {
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.line-clamp-3 {
  display: -webkit-box;
  -webkit-line-clamp: 3;
  -webkit-box-orient: vertical;
  overflow: hidden;
}
</style>