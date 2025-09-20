<template>
  <div class="min-h-screen bg-white">
    <!-- Header Section -->
    <div class="bg-white py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-2xl">
          <h1 class="text-4xl md:text-5xl font-bold text-gray-900 mb-6">{{ $t('contact.title') }}</h1>
          <p class="text-lg text-gray-600 leading-relaxed">
            {{ $t('contact.description') }}
          </p>
        </div>
      </div>
    </div>

    <!-- Contact Form Section -->
    <div class="bg-gray-50 py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-2xl mx-auto">
          <ContactForm />
        </div>
      </div>
    </div>

    <!-- Other Ways to Reach Us -->
    <div class="bg-white py-16">
      <div class="container mx-auto px-4">
        <div class="max-w-2xl mx-auto">
          <h2 class="text-2xl font-bold text-gray-900 mb-8">{{ $t('contact.getInTouch') }}</h2>
          
          <div class="space-y-6">
            <!-- Email -->
            <div class="flex items-start space-x-4">
              <div class="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 8l7.89 4.26a2 2 0 002.22 0L21 8M5 19h14a2 2 0 002-2V7a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 mb-1">{{ $t('contact.email') }}</h3>
                <p class="text-blue-600 hover:text-blue-800">support@studyhub.com</p>
              </div>
            </div>

            <!-- Phone -->
            <div class="flex items-start space-x-4">
              <div class="w-12 h-12 bg-gray-100 rounded-xl flex items-center justify-center flex-shrink-0">
                <svg class="w-6 h-6 text-gray-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M3 5a2 2 0 012-2h3.28a1 1 0 01.948.684l1.498 4.493a1 1 0 01-.502 1.21l-2.257 1.13a11.042 11.042 0 005.516 5.516l1.13-2.257a1 1 0 011.21-.502l4.493 1.498a1 1 0 01.684.949V19a2 2 0 01-2 2h-1C9.716 21 3 14.284 3 6V5z" />
                </svg>
              </div>
              <div>
                <h3 class="text-lg font-semibold text-gray-900 mb-1">{{ $t('contact.phone') }}</h3>
                <p class="text-blue-600 hover:text-blue-800">+1 (555) 123-4567</p>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import ContactForm from '@/components/contact/ContactForm.vue'
import ContactInfo from '@/components/contact/ContactInfo.vue'
</script>

<style scoped>
.contact-page {
  min-height: 100vh;
}
</style>