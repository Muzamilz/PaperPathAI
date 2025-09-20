<template>
  <div class="min-h-screen bg-white">
    <!-- Header Section -->
    <div class="bg-white py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-2xl">
          <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6">Request Assistance</h1>
          <p class="text-lg text-gray-600 leading-relaxed">
            Please fill out the form below to submit your request. We'll get back to you within 24 hours.
          </p>
        </div>
      </div>
    </div>

    <!-- Form Section -->
    <div class="bg-gray-50 py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-2xl mx-auto">
          <ServiceRequestForm :service-id="serviceId" />
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ServiceRequestForm from '@/components/services/ServiceRequestForm.vue'

// Props
const props = defineProps({
  serviceId: {
    type: [String, Number],
    default: null
  }
})
</script>