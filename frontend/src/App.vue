<template>
  <div id="app" :class="{ 'rtl': isRTL }" :dir="direction">
    <AppLayout>
      <RouterView />
    </AppLayout>
    
    <!-- Global Notification System -->
    <NotificationSystem ref="notificationSystem" />
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { RouterView } from 'vue-router'
import AppLayout from '@/components/layout/AppLayout.vue'
import NotificationSystem from '@/components/ui/NotificationSystem.vue'

const { locale } = useI18n()

const isRTL = computed(() => locale.value === 'ar')
const direction = computed(() => isRTL.value ? 'rtl' : 'ltr')
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

.rtl {
  direction: rtl;
}

/* Global RTL support */
.rtl * {
  direction: rtl;
}

/* Tailwind RTL utilities */
.rtl .space-x-reverse > :not([hidden]) ~ :not([hidden]) {
  --tw-space-x-reverse: 1;
}

.rtl .divide-x-reverse > :not([hidden]) ~ :not([hidden]) {
  --tw-divide-x-reverse: 1;
}
</style>