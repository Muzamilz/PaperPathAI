<template>
  <div class="portfolio-gallery">
    <!-- Loading State -->
    <div v-if="loading" class="flex justify-center items-center py-12">
      <div class="animate-spin rounded-full h-12 w-12 border-b-2 border-blue-600"></div>
    </div>

    <!-- Error State -->
    <div v-else-if="error" class="text-center py-12">
      <div class="text-red-600 mb-4">{{ error }}</div>
      <button @click="fetchPortfolioItems" class="btn btn-primary">
        {{ $t('common.retry') }}
      </button>
    </div>

    <!-- Portfolio Grid -->
    <div v-else-if="filteredItems && filteredItems.length" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8">
      <PortfolioCard
        v-for="item in filteredItems"
        :key="item.id"
        :item="item"
        @click="openModal(item)"
        class="cursor-pointer"
      />
    </div>

    <!-- Empty State -->
    <div v-else class="text-center py-12">
      <div class="text-gray-500 mb-4">
        {{ selectedCategory ? $t('portfolio.noItemsInCategory') : $t('portfolio.noItems') }}
      </div>
      <button v-if="selectedCategory" @click="clearFilters" class="btn btn-secondary">
        {{ $t('portfolio.showAll') }}
      </button>
    </div>

    <!-- Portfolio Detail Modal -->
    <PortfolioModal
      v-if="selectedItem"
      :item="selectedItem"
      @close="closeModal"
    />
  </div>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { usePortfolioStore } from '@/stores/portfolio'
import PortfolioCard from './PortfolioCard.vue'
import PortfolioModal from './PortfolioModal.vue'

const props = defineProps({
  selectedCategory: {
    type: String,
    default: 'all'
  }
})

const portfolioStore = usePortfolioStore()

// Computed properties from store
const loading = computed(() => portfolioStore.loading)
const error = computed(() => portfolioStore.error)
const filteredItems = computed(() => {
  const items = portfolioStore.items || []
  if (props.selectedCategory === 'all') {
    return items
  }
  return items.filter(item => 
    item.category?.slug === props.selectedCategory
  )
})
const selectedItem = computed(() => portfolioStore.currentItem)

// Methods
const fetchPortfolioItems = () => {
  portfolioStore.fetchPortfolioItems()
}

const clearFilters = () => {
  // This would be handled by parent component
}

const openModal = (item) => {
  portfolioStore.currentItem = item
}

const closeModal = () => {
  portfolioStore.currentItem = null
}

// Lifecycle
onMounted(() => {
  fetchPortfolioItems()
})
</script>

<style scoped>
.btn {
  @apply px-4 py-2 rounded-lg font-medium transition-colors duration-200;
}

.btn-primary {
  @apply bg-blue-600 text-white hover:bg-blue-700;
}

.btn-secondary {
  @apply bg-gray-600 text-white hover:bg-gray-700;
}
</style>