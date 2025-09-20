<template>
  <div :dir="languageStore.direction" :class="{ 'rtl': languageStore.direction === 'rtl' }">
    <router-view />
  </div>
</template>

<script setup>
import { useLanguageStore } from '@/stores/language'

const languageStore = useLanguageStore()
</script>

<style>
.rtl {
  direction: rtl;
}
</style>