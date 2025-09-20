<template>
  <div class="min-h-screen bg-white">
    <!-- Header Section -->
    <div class="bg-white py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-4xl">
          <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6">{{ $t('services.title') }}</h1>
          <p class="text-lg text-gray-600 leading-relaxed">
            {{ $t('services.description') }}
          </p>
        </div>
      </div>
    </div>

    <!-- Services Catalog -->
    <div class="bg-gray-50 py-16">
      <div class="container mx-auto px-4">
        <ServiceCatalog />
      </div>
    </div>
  </div>
</template>

<script setup>
import ServiceCatalog from '@/components/services/ServiceCatalog.vue'
</script>