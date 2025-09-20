<template>
  <div class="min-h-screen flex flex-col" :class="layoutClasses">
    <!-- Header -->
    <AppHeader />
    
    <!-- Main Content -->
    <main class="flex-1 bg-gray-50">
      <slot />
    </main>
    
    <!-- Footer -->
    <AppFooter />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useLanguageStore } from '@/stores/language'
import AppHeader from './AppHeader.vue'
import AppFooter from './AppFooter.vue'

const languageStore = useLanguageStore()

// Computed properties for layout classes
const layoutClasses = computed(() => ({
  'rtl': languageStore.isRTL,
  'font-arabic': languageStore.currentLanguage === 'ar',
  'font-english': languageStore.currentLanguage === 'en'
}))
</script>

<style scoped>
/* Font families for different languages */
.font-arabic {
  font-family: 'Noto Sans Arabic', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

.font-english {
  font-family: 'Inter', 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
}

/* RTL-specific adjustments */
.rtl {
  direction: rtl;
}

/* Ensure proper text alignment */
.rtl * {
  text-align: right;
}

.rtl .text-left {
  text-align: right !important;
}

.rtl .text-right {
  text-align: left !important;
}

/* Fix for flex direction in RTL */
.rtl .flex-row {
  flex-direction: row-reverse;
}

.rtl .space-x-reverse > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}
</style>