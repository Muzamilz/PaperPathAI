<template>
  <div class="min-h-screen bg-white">
    <!-- Header Section -->
    <div class="bg-white py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl">
          <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6">{{ $t('portfolio.title') }}</h1>
          <p class="text-lg text-gray-600 leading-relaxed">
            {{ $t('portfolio.description') }}
          </p>
        </div>
      </div>
    </div>

    <!-- Filter Tabs -->
    <div class="bg-gray-50 border-b">
      <div class="container mx-auto px-4">
        <div class="flex space-x-8 overflow-x-auto">
          <button
            v-for="category in categories"
            :key="category.value"
            @click="selectedCategory = category.value"
            :class="[
              'py-4 px-2 border-b-2 font-medium text-sm whitespace-nowrap transition-colors duration-200',
              selectedCategory === category.value
                ? 'border-blue-600 text-blue-600'
                : 'border-transparent text-gray-500 hover:text-gray-700 hover:border-gray-300'
            ]"
          >
            {{ category.label }}
          </button>
        </div>
      </div>
    </div>

    <!-- Portfolio Gallery -->
    <div class="container mx-auto px-4 py-16">
      <PortfolioGallery :selected-category="selectedCategory" />
    </div>

    <!-- Pagination -->
    <div class="container mx-auto px-4 pb-16">
      <div class="flex justify-center items-center space-x-2">
        <button class="p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200">
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
          </svg>
        </button>
        
        <button
          v-for="page in [1, 2, 3]"
          :key="page"
          :class="[
            'px-4 py-2 rounded-lg font-medium transition-colors duration-200',
            page === 1
              ? 'bg-blue-600 text-white'
              : 'text-gray-600 hover:bg-gray-100'
          ]"
        >
          {{ page }}
        </button>
        
        <span class="px-2 text-gray-400">...</span>
        <button class="px-4 py-2 rounded-lg font-medium text-gray-600 hover:bg-gray-100 transition-colors duration-200">
          10
        </button>
        
        <button class="p-2 rounded-lg hover:bg-gray-100 transition-colors duration-200">
          <svg class="w-5 h-5 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 5l7 7-7 7" />
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import PortfolioGallery from '@/components/portfolio/PortfolioGallery.vue'

// State
const selectedCategory = ref('all')

// Categories for filtering
const categories = [
  { value: 'all', label: 'All' },
  { value: 'research', label: 'Research Assistance' },
  { value: 'project', label: 'Project Help' },
  { value: 'academic', label: 'Academic Support' }
]
</script>

<style scoped>
.portfolio-page {
  min-height: 100vh;
}
</style>