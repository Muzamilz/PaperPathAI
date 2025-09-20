<template>
  <div class="fixed bottom-6 right-6 z-40" :class="{ 'bottom-6 left-6 right-auto': isRTL }">
    <!-- Main FAB -->
    <button
      @click="toggleMenu"
      class="fab group"
      :class="{ 'rotate-45': isOpen }"
    >
      <svg 
        class="w-6 h-6 transition-transform duration-200" 
        :class="{ 'rotate-45': isOpen }"
        fill="none" 
        stroke="currentColor" 
        viewBox="0 0 24 24"
      >
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 6v6m0 0v6m0-6h6m-6 0H6" />
      </svg>
    </button>

    <!-- Sub-actions -->
    <transition-group
      name="fab-item"
      tag="div"
      class="absolute bottom-16 right-0 space-y-3"
      :class="{ 'right-auto left-0': isRTL }"
    >
      <div
        v-for="(action, index) in actions"
        v-show="isOpen"
        :key="action.id"
        class="flex items-center"
        :class="{ 'flex-row-reverse': isRTL }"
        :style="{ transitionDelay: `${index * 50}ms` }"
      >
        <!-- Action Label -->
        <div 
          class="bg-gray-900 text-white text-sm px-3 py-2 rounded-lg mr-3 whitespace-nowrap shadow-lg"
          :class="{ 'mr-0 ml-3': isRTL }"
        >
          {{ action.label }}
        </div>
        
        <!-- Action Button -->
        <button
          @click="handleAction(action)"
          class="w-12 h-12 rounded-full shadow-lg flex items-center justify-center text-white transition-all duration-200 hover:scale-110 active:scale-95"
          :class="action.color"
        >
          <component :is="action.icon" class="w-5 h-5" />
        </button>
      </div>
    </transition-group>

    <!-- Backdrop -->
    <div
      v-if="isOpen"
      @click="closeMenu"
      class="fixed inset-0 bg-black bg-opacity-20 -z-10"
    ></div>
  </div>
</template>

<script setup>
import { ref, computed, h } from 'vue'
import { useRouter } from 'vue-router'
import { useI18n } from 'vue-i18n'
import { useLanguageStore } from '@/stores/language'

const { t: $t } = useI18n()

const router = useRouter()
const languageStore = useLanguageStore()

const isOpen = ref(false)
const isRTL = computed(() => languageStore.direction === 'rtl')

// Define available actions
const actions = ref([
  {
    id: 'contact',
    label: computed(() => $t('contact.title')),
    color: 'bg-blue-500 hover:bg-blue-600',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z' })
    ]),
    action: () => {
      const contactSection = document.querySelector('#contact-section')
      if (contactSection) {
        contactSection.scrollIntoView({ behavior: 'smooth' })
      }
    }
  },
  {
    id: 'request',
    label: computed(() => $t('services.requestService')),
    color: 'bg-green-500 hover:bg-green-600',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M12 6v6m0 0v6m0-6h6m-6 0H6' })
    ]),
    action: () => {
      router.push(languageStore.getLocalizedRoute('ServiceRequest'))
    }
  },
  {
    id: 'chat',
    label: computed(() => $t('fab.liveChat')),
    color: 'bg-purple-500 hover:bg-purple-600',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M8 12h.01M12 12h.01M16 12h.01M21 12c0 4.418-4.03 8-9 8a9.863 9.863 0 01-4.255-.949L3 20l1.395-3.72C3.512 15.042 3 13.574 3 12c0-4.418 4.03-8 9-8s9 3.582 9 8z' })
    ]),
    action: () => {
      if (window.$notify) {
        window.$notify.info($t('fab.comingSoon'), $t('fab.chatSoon'))
      }
    }
  },
  {
    id: 'phone',
    label: computed(() => $t('fab.callUs')),
    color: 'bg-orange-500 hover:bg-orange-600',
    icon: () => h('svg', { fill: 'none', stroke: 'currentColor', viewBox: '0 0 24 24' }, [
      h('path', { 'stroke-linecap': 'round', 'stroke-linejoin': 'round', 'stroke-width': '2', d: 'M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z' })
    ]),
    action: () => {
      window.open('tel:+1234567890', '_self')
    }
  }
])

const toggleMenu = () => {
  isOpen.value = !isOpen.value
}

const closeMenu = () => {
  isOpen.value = false
}

const handleAction = (action) => {
  action.action()
  closeMenu()
}
</script>

<style scoped>
.fab-item-enter-active,
.fab-item-leave-active {
  transition: all 0.3s ease;
}

.fab-item-enter-from,
.fab-item-leave-to {
  opacity: 0;
  transform: translateY(20px) scale(0.8);
}

.fab-item-move {
  transition: transform 0.3s ease;
}
</style>